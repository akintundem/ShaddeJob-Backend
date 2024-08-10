import pika
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def wait_for_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            logging.info("RabbitMQ is ready!")
            return connection
        except pika.exceptions.AMQPConnectionError:
            logging.info("RabbitMQ is not ready yet. Waiting...")
            time.sleep(5)

def process_resume(ch, method, properties, body):
    logging.info(f"Received message: {body.decode()}")
    # Simulate processing
    time.sleep(5)  # Simulate processing time
    logging.info(f"Processed message: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def resume_consumer(connection, queue_name):
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=process_resume)
    
    logging.info('Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    logging.info("Starting Receiver")
    connection = wait_for_rabbitmq()
    resume_consumer(connection, 'test_queue')
