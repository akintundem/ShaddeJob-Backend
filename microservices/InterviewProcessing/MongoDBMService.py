from pymongo import MongoClient
import uuid
from datetime import datetime

class UsersDBService:
    def __init__(self, mongo_uri, db_name, collection_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def get_job_description(self, user_id):
        user = self.collection.find_one({"user_id": user_id}, {"jobDescription": 1})
        return user.get("jobDescription") if user else None

    def get_summary_of_resume(self, user_id):
        user = self.collection.find_one({"user_id": user_id}, {"summaryOfResume": 1})
        return user.get("summaryOfResume") if user else None

    



class ConversationDBService:
    def __init__(self, mongo_uri, db_name, collection_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_chat_session(self, user_id,system_instructions):
        """Create a new chat session and store it in MongoDB."""
        session = {
            "chat_id": str(uuid.uuid4()),
            "user_id": user_id,
            "system_instruction": system_instructions,
            "timestamp": datetime.now(),
            "messages": []
        }
        self.collection.insert_one(session)
        return session["chat_id"]

    def update_chat_session(self, chat_id, sender, message):
        """Update the chat session with a new message."""
        self.collection.update_one(
            {"chat_id": chat_id},
            {"$push": {"messages": {"sender": sender, "message": message, "timestamp": datetime.utcnow()}}}
        )

    def get_chat_info(self, chat_id):
        """Retrieve chat history from MongoDB."""
        return self.collection.find_one({"chat_id": chat_id})

    def get_last_user_input(self, chat_id, user_id):
            """Retrieve the last user input based on chat_id and user_id."""
            chat = self.collection.find_one(
                {"chat_id": chat_id, "user_id": user_id},
                {"messages": {"$slice": -1}}
            )
            if chat and chat["messages"]:
                last_message = chat["messages"][-1]
                if last_message["sender"] == "user":
                    return last_message["message"]
            return None