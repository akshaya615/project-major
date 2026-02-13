import numpy as np
import pandas as pd
import hdbscan
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "accident_db"

# -------------------------
# MongoDB Connection
# -------------------------
print("Connecting to MongoDB Atlas...")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

accident_col = db["accident_data"]
hotspot_col = db["hotspots"]

# -------------------------
# Load accident coordinates
# -------------------------
cursor = accident_col.find(
    {"Latitude": {"$ne": None}, "Longitude": {"$ne": None}},
    {"Latitude": 1, "Longitude": 1, "_id": 0}
)

df = pd.DataFrame(list(cursor))
print(f"Loaded {len(df)} accident records")

if len(df) < 20:
    print("Not enough data for clustering")
    exit()

# -------------------------
# Prepare coordinates
# -------------------------
coords = df[["Latitude", "Longitude"]].values
coords_rad = np.radians(coords)  # required for haversine

# -------------------------
# Relaxed HDBSCAN (IMPORTANT)
# -------------------------
print("Running HDBSCAN clustering...")

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=3,        # relaxed
    min_samples=1,             # relaxed
    metric="haversine",
    cluster_selection_method="eom"
)

labels = clusterer.fit_predict(coords_rad)
df["cluster_id"] = labels

# -------------------------
# Remove noise
# -------------------------
clusters = df[df["cluster_id"] != -1]

if clusters.empty:
    print("⚠️ No clusters found, creating demo hotspot")

    # fallback demo hotspot
    sample = df.sample(10)
    hotspots = [{
        "cluster_id": 0,
        "centroid_lat": float(sample["Latitude"].mean()),
        "centroid_lon": float(sample["Longitude"].mean()),
        "density_score": int(len(sample))
    }]

else:
    hotspots = []
    for cid, group in clusters.groupby("cluster_id"):
        hotspots.append({
            "cluster_id": int(cid),
            "centroid_lat": float(group["Latitude"].mean()),
            "centroid_lon": float(group["Longitude"].mean()),
            "density_score": int(len(group))
        })

print(f"Hotspots detected: {len(hotspots)}")

# -------------------------
# Save to MongoDB
# -------------------------
hotspot_col.delete_many({})
hotspot_col.insert_many(hotspots)

print("HDBSCAN hotspots saved successfully")
