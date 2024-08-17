from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDBClient:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
    
    def save_to_mongodb(self, collection_name, key, data, document_id=None):

            collection = self.db[collection_name]

            if document_id:
                # Ensure document_id is a string
                if not isinstance(document_id, str):
                    print("Error: document_id must be a string.")
                    return None

                try:
                    # Convert document_id to ObjectId
                    object_id = ObjectId(document_id)
                except Exception as e:
                    print(f"Error converting document_id to ObjectId: {e}")
                    return None

                # Update the document with the new data
                result = collection.update_one({'_id': object_id}, {'$set': {key:data}}, upsert=False)
                return document_id if result.modified_count > 0 else None
        
    def load_from_mongodb(self, collection_name, query):
        """
        Load data from MongoDB based on a query.
        
        :param collection_name: The name of the collection from which data will be loaded.
        :param query: The query to find the data. Should be a dictionary.
        :return: The found document, or None if no document matches the query.
        """
        collection = self.db[collection_name]
        result = collection.find_one(query)
        return result

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()

