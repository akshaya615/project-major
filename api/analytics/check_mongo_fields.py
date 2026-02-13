from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["accident_db"]

doc = db["accident_data"].find_one()

print("Sample MongoDB document:")
for k in doc.keys():
    print(k)
