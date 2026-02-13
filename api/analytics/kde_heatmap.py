import pandas as pd
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from sklearn.neighbors import KernelDensity

# ---------------------------------------
# Load environment variables
# ---------------------------------------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# ---------------------------------------
# MongoDB connection
# ---------------------------------------
print("Connecting to MongoDB Atlas...")
client = MongoClient(MONGO_URI)
db = client["accident_db"]

accident_col = db["accident_data"]
kde_col = db["kde_heatmap"]

# ---------------------------------------
# Load coordinates
# ---------------------------------------
cursor = accident_col.find(
    {},
    {"_id": 0, "Latitude": 1, "Longitude": 1}
)

df = pd.DataFrame(list(cursor))
df = df.dropna(subset=["Latitude", "Longitude"])

coords = df[["Latitude", "Longitude"]].values
coords_rad = np.radians(coords)

# ---------------------------------------
# KDE modeling
# ---------------------------------------
print("Running KDE heatmap generation...")

kde = KernelDensity(
    bandwidth=0.02,     # adjust if needed
    kernel="gaussian",
    metric="haversine"
)

kde.fit(coords_rad)

# Generate grid
lat_min, lon_min = coords.min(axis=0)
lat_max, lon_max = coords.max(axis=0)

lat_grid = np.linspace(lat_min, lat_max, 100)
lon_grid = np.linspace(lon_min, lon_max, 100)

lat_mesh, lon_mesh = np.meshgrid(lat_grid, lon_grid)
grid_coords = np.vstack([lat_mesh.ravel(), lon_mesh.ravel()]).T
grid_rad = np.radians(grid_coords)

density = np.exp(kde.score_samples(grid_rad))

heatmap_df = pd.DataFrame({
    "Latitude": grid_coords[:, 0],
    "Longitude": grid_coords[:, 1],
    "Density": density
})

# ---------------------------------------
# Store KDE heatmap in MongoDB
# ---------------------------------------
kde_col.delete_many({})
kde_col.insert_many(heatmap_df.to_dict(orient="records"))

print("KDE heatmap data stored in MongoDB")
