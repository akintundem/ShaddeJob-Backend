import os
import json

from GeminiService import GeminiService
from MongoDBMService import UsersDBService,ConversationDBService
from RabbitMQManager import RabbitMQManager 

class ChatBot:
    def __init__(self, gemini_service, mongo_service):
        self.gemini_service = gemini_service
        self.mongo_service = mongo_service

    def create_chat_session(self, user_id,system_instructions):
        return self.mongo_service.create_chat_session(user_id,system_instructions)

    def format_history_for_chat(self, history):
        formatted_history = []
        for entry in history:
            if entry['sender'] == 'user':
                formatted_history.append({"user": entry['message']})
            else:
                formatted_history.append({"bot": entry['message']})
        return formatted_history

    def handle_user_input(self, chat_id, user_input):
        system_instructions = self.mongo_service.get_chat_info(chat_id)["system_instruction"]
        self.mongo_service.update_chat_session(chat_id, "user", user_input)
        history = self.mongo_service.get_chat_info(chat_id)["messages"]
        # history = self.format_history_for_chat(history)
        response = self.gemini_service.generate_response(system_instructions,history, user_input).text
        self.mongo_service.update_chat_session(chat_id, "bot", response)
        return response

    def get_chat_history(self, chat_id):
        return self.mongo_service.get_chat_history(chat_id)

def load_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def setup_system_instruction(file_name, jobDescription, summaryOfResume):
    try:
        system_instructions_template = load_file(file_name)
        if system_instructions_template:
            return system_instructions_template.replace("${jobDescription}", jobDescription).replace("${summaryOfResume}", summaryOfResume)
    except Exception as e:
        print(f"An error occurred while setting up the system instructions: {e}")
        return None


if __name__ == "__main__":
    # listen for instructions from the master API
    rabbitmq_manager = RabbitMQManager()
    rabbitmq_manager.initialize_rabbitmq()

    api_key = os.getenv("GEMINI_API_KEY")
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")
    conversations_collection_name = os.getenv("conversations_collection_name")
    users_collection_name = os.getenv("users_collection_name")
    system_instructions_file_name = "system_instruction.txt"

    gemini_service = GeminiService(api_key)
    conversation_db_service = ConversationDBService(mongo_uri, db_name, conversations_collection_name)
    users_db_service = UsersDBService(mongo_uri, db_name, users_collection_name)
    chatbot = ChatBot(gemini_service, conversation_db_service)

    def on_message_callback(ch, method, properties, body):        
        parsed_message = json.loads(body.decode())
        messageId = parsed_message['messageId']
        action = parsed_message['action']
        ch.basic_ack(delivery_tag=method.delivery_tag)

        if action == "StartChat":
            user_id = parsed_message['user_id']
            jobDescription = users_db_service.get_job_description(user_id)
            summaryOfResume = users_db_service.get_summary_of_resume(user_id)
            system_instructions = setup_system_instruction(system_instructions_file_name, jobDescription, summaryOfResume)
            chat_id = chatbot.create_chat_session(user_id,system_instructions)
            message = {
                "action": "Chat_Started",
                "chat_id": chat_id
            }
            rabbitmq_manager.send_message(json.dumps(message),messageId)
        elif action == "ConstChat":
            chat_id = parsed_message['chat_id']
            user_id = parsed_message['user_id']
            user_input = conversation_db_service.get_last_user_input(chat_id,user_id)
            chatbot.handle_user_input(user_id, chat_id, user_input)
            message = {
                "action": "Bot_Responded",
                "chat_id": chat_id
            }
            rabbitmq_manager.send_message(json.dumps(message),messageId)

    rabbitmq_manager.consumer('Interview_Chat', on_message_callback)
