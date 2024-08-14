import pika
import time
import logging
import docx
import PyPDF2
import ollama
import json
import requests



connection = None
channel = None


def convert_resume_to_text(file_path):
    # Check if the resume format is .pdf
    logging.info(file_path)
    logging.info(file_path.split(".")[1].lower())
    if file_path.split(".")[1].lower() == 'pdf':
        # Open the PDF file and scrape all the text
        logging.info("we aer in")
        try:
            with open(file_path, 'rb') as pdf_file:
                totalText = ""
                reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    totalText += text
                return totalText
        except Exception as e:
            logging.info(f"Error reading PDF: {e}")
            return None
    
    # Check if the resume format is .docx
    elif file_path.split(".")[1].lower() == 'docx':
        try:
            doc = docx.Document(file_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return None
    
    # If the format is neither .pdf nor .docx
    else:
        print("Unsupported file format")
        return None


def generate_response(prompt):
    url = "http://host.docker.internal:11434/api/generate"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3",
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=data
        )
        
        # Check if the response status code indicates an error
        response.raise_for_status()
        
        # Parse and return the JSON response
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        logging.info(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.info(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
       logging.info(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.info(f"An error occurred: {req_err}")
    except Exception as err:
        logging.info(f"An unexpected error occurred: {err}")





def convert_resume_to_json(textResume):
    prompt = f"""
    I have provided the following resume text. Please extract the following information and format it as a JSON object with the following keys: "skills", "education", "volunteering", "experience", and "certifications". Each key should contain an array of relevant entries.

    Resume:
    {textResume}

    JSON Output:
    {{
      "skills": [],
      "education": [],
      "volunteering": [],
      "experience": [],
      "certifications": []
    }}
    """
    return generate_response(prompt)
    
def initialize_rabbitmq():
    global connection, channel
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq')) 
            channel = connection.channel()
            logging.info("RabbitMQ is ready!")
            return
        except pika.exceptions.AMQPConnectionError:
            logging.info("RabbitMQ is not ready yet. Waiting...")
            time.sleep(5)

def get_rabbitmq_channel():
    global channel
    if channel is None or not channel.is_open:
        return None
    return channel

def send_message_via_rabbitmq_to_master_server(message, queue_name):
    try:
        ch = get_rabbitmq_channel()
        ch.basic_publish(
            exchange='',
            routing_key=queue_name,  
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2 
            )
        )
        logging.info(f"Sent message to RabbitMQ: {message}")
    except Exception as e:
        logging.error(f"Error sending message to RabbitMQ: {e}")

def resume_consumer(connection,queue_name):
    ch = get_rabbitmq_channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=process_resume)
    
    logging.info('Waiting for messages. To exit press CTRL+C')
    try:
        ch.start_consuming()
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()

def process_resume(ch, method, properties, body):

    # we will be putting this whole code into threads. 

    logging.info(f"Received message: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    parsed_message = json.loads(body.decode())
    user_id = parsed_message['messageId']
    received_message = parsed_message['filePath']

    textResume = convert_resume_to_text(received_message)
    jsonResume = json.dumps(convert_resume_to_json(textResume))["response"]
    # send_message = jsonResume['message']['content'] 
    # print(send_message)

    send_message = jsonResume

    logging.info(f"Processed message: {send_message}")

    send_message_via_rabbitmq_to_master_server(send_message, user_id)  



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting Receiver")
    initialize_rabbitmq()
    if get_rabbitmq_channel() is not None:
        resume_consumer(connection,"send_resume_to_process_container")