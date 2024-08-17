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
        request_id = parsed_message['messageId']
        user_id = "66af2e71a27d07775a327421"
        action = parsed_message['action']
        
        if action == "ResumeJSON":
            self._process_resume_json(parsed_message, user_id)
        elif action == "CoverLetterGeneration":
            self._process_cover_letter_generation(parsed_message,user_id)
        
    def _process_resume_json(self, parsed_message, user_id):
        text_resume = self.resume_processor.convert_resume_to_text(parsed_message)
        
        if text_resume:
            resume_json = self.resume_processor.generate_response("kyc_system_instruction", text_resume)
            resume_summary  = json.loads(resume_json.text.strip().lstrip('```json').strip('```').strip())
            self.mongo_manager.save_to_mongodb("users","resume_json",resume_summary, user_id)

            resume_summary = self.resume_processor.generate_response("summary_system_instruction", text_resume).text
            self.mongo_manager.save_to_mongodb("users","resume_summary",resume_summary, user_id)
           
            self.rabbitmq_manager.send_message("ResumeComplete", user_id)


    def _process_cover_letter_generation(self, parsed_message, user_id):
        resume_data = self.resume_processor.convert_resume_to_text(parsed_message)
        cover_letter = self.resume_processor.generate_response("cover_letter_system_instruction", resume_data)
        self.mongo_manager.save_to_mongodb(user_id, "cover_letter", cover_letter.text)
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
    prompt_loader = load_prompt_from_file('prompts.json')

    rabbitmq_manager = RabbitMQManager()
    mongo_manager = MongoDBClient(mongo_uri, db_name)
    resume_processor = ResumeProcessor(api_key, prompt_loader)
    main_processor = MainProcessor(rabbitmq_manager, resume_processor, mongo_manager)

    rabbitmq_manager.initialize_rabbitmq()
    if rabbitmq_manager.get_channel() is not None:
        main_processor = MainProcessor(rabbitmq_manager, resume_processor, mongo_manager)
        main_processor.start("contact_genai_for_processing")