from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pathlib import Path

# 🔥 Force load .env from api folder
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")

print("Loaded Mongo URI:", MONGO_URI)

DB_NAME = "accident_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

accident_col = db["accident_data"]
hotspot_col = db["hotspots"]
kde_col = db["kde_heatmap"]
alert_col = db["alerts"]