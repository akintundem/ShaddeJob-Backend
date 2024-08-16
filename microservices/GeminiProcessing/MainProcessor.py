import os
import logging
import json

from RabbitMQManager import RabbitMQManager
from MongoDBManager import MongoDBClient
from ResumeProcessor import ResumeProcessor

class MainProcessor:
    def __init__(self, rabbitmq_manager, resume_processor, mongo_manager):
        self.rabbitmq_manager = rabbitmq_manager
        self.resume_processor = resume_processor
        self.mongo_manager = mongo_manager

    def process_resume(self, ch, method, properties, body):
        logging.info(f"Received message: {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

        parsed_message = json.loads(body.decode())
        user_id = parsed_message['messageId']
        action = parsed_message['action']
        
        if action == "ResumeJSON":
            self._process_resume_json(parsed_message, user_id)
        elif action == "CoverLetterGeneration":
            self._process_cover_letter_generation(user_id)
        
    def _process_resume_json(self, parsed_message, user_id):
        received_message = parsed_message['filePath']
        text_resume = self.resume_processor.convert_resume_to_text(received_message)
        
        if text_resume:
            message_json = self.resume_processor.generate_response("kyc_system_instruction", text_resume)
            self.mongo_manager.save_to_mongodb(user_id, "resume_json", message_json["response"])

            resume_summary = self.resume_processor.generate_response("summary_system_instruction", text_resume)
            self.mongo_manager.save_to_mongodb(user_id, "resume_summary", resume_summary["response"])
           
            self.rabbitmq_manager.send_message("ResumeComplete", user_id)


    def _process_cover_letter_generation(self, user_id):
        resume_data = self.mongo_manager.load_from_mongodb(user_id, "resume_json")
        cover_letter = self.resume_processor.generate_response("cover_letter_system_instruction", resume_data)
        self.mongo_manager.save_to_mongodb(user_id, "cover_letter", cover_letter["response"])
        self.rabbitmq_manager.send_message("CoverLetterComplete", user_id)

    def start(self, queue_name):
        self.rabbitmq_manager.resume_consumer(queue_name, self.process_resume)

def load_prompt_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting Gemini Client")

    api_key = os.getenv("GEMINI_API_KEY")
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")
    prompt_loader = load_prompt_from_file('prompts.txt')
    
    rabbitmq_manager = RabbitMQManager()
    mongo_manager = MongoDBClient(mongo_uri, db_name)
    resume_processor = ResumeProcessor(api_key, prompt_loader.system_instructions)
    
    rabbitmq_manager.initialize_rabbitmq()
    if rabbitmq_manager.get_channel() is not None:
        main_processor = MainProcessor(rabbitmq_manager, resume_processor, mongo_manager)
        main_processor.start("contact_genai_for_processing")
