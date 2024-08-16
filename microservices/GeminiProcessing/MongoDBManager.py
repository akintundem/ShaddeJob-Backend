from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDBClient:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def save_to_mongodb(self, collection_name, data, document_id=None):
        """
        Save data to MongoDB. If document_id is provided, update the document.
        Otherwise, insert a new document.
        
        :param collection_name: The name of the collection where data will be saved.
        :param data: The data to save. Should be a dictionary.
        :param document_id: Optional. The ID of the document to update. If not provided, a new document is created.
        :return: The ID of the saved document.
        """
        collection = self.db[collection_name]
        
        if document_id:
            result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': data}, upsert=True)
            return document_id if result.modified_count > 0 else None
        else:
            result = collection.insert_one(data)
            return str(result.inserted_id)

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

# # Usage Example:
# if __name__ == "__main__":
#     # Replace with your MongoDB URI and database name
#     mongo_uri = "mongodb://localhost:27017"
#     db_name = "my_database"
    
#     # Create a MongoDB client instance
#     mongo_client = MongoDBClient(mongo_uri, db_name)
    
#     # Example of saving data
#     user_id = "user123"
#     data_to_save = {
#         "name": "John Doe",
#         "email": "john.doe@example.com"
#     }
#     document_id = mongo_client.save_to_mongodb("users", data_to_save)
#     print(f"Saved document with ID: {document_id}")
    
#     # Example of loading data
#     loaded_data = mongo_client.load_from_mongodb("users", {"_id": ObjectId(document_id)})
#     print("Loaded Data:", loaded_data)
    
#     # Close the MongoDB connection
#     mongo_client.close_connection()
