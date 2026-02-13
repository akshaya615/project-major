from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

print("Connecting to MongoDB Atlas...")
client = MongoClient(MONGO_URI)

db = client["accident_db"]

print("Connected successfully!")
print("Collections:", db.list_collection_names())
