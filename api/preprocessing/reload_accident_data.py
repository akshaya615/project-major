import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["accident_db"]

accident_col = db["accident_data"]

print("Loading dataset with coordinates...")

df = pd.read_csv("processed_accident_with_coords.csv")

print("Columns in CSV:", df.columns.tolist())

records = df.to_dict(orient="records")

# Replace existing data
accident_col.delete_many({})
accident_col.insert_many(records)

print(f"Inserted {len(records)} accident records WITH coordinates")
