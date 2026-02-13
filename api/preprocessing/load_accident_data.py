import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "accident_db"

print("Connecting to MongoDB Atlas...")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

collection = db["accident_data"]

# Load cleaned dataset
df = pd.read_csv("cleaned_accident.csv")

# Convert dataframe to dict
records = df.to_dict(orient="records")

# Insert into MongoDB
if records:
    collection.insert_many(records)
    print(f"Inserted {len(records)} accident records")
else:
    print("No records found to insert")

print("Current collections:", db.list_collection_names())
