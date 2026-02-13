from api.core.database import accident_col, hotspot_col
from datetime import datetime
import numpy as np
from sklearn.cluster import DBSCAN

def recompute_hotspots():
    """
    Recalculate accident hotspots using DBSCAN
    Runs in background scheduler
    """

    print("🔥 Recomputing hotspots...")

    accidents = list(accident_col.find({}, {"_id": 0}))

    if len(accidents) < 5:
        print("⚠️ Not enough accident data")
        return

    # ----------------------------------
    # Prepare coordinates
    # ----------------------------------
    coords = []
    for a in accidents:
        if "latitude" in a and "longitude" in a:
            coords.append([a["latitude"], a["longitude"]])

    if len(coords) < 5:
        print("⚠️ Not enough valid coordinates")
        return

    X = np.array(coords)

    # ----------------------------------
    # DBSCAN clustering
    # ----------------------------------
    clustering = DBSCAN(
        eps=0.005,        # ~500m radius
        min_samples=5
    ).fit(X)

    labels = clustering.labels_

    # ----------------------------------
    # Clear old hotspots
    # ----------------------------------
    hotspot_col.delete_many({})
    print("🧹 Old hotspots cleared")

    # ----------------------------------
    # Insert new hotspots
    # ----------------------------------
    unique_labels = set(labels)

    for label in unique_labels:
        if label == -1:
            continue

        cluster_points = X[labels == label]

        centroid_lat = float(cluster_points[:, 0].mean())
        centroid_lon = float(cluster_points[:, 1].mean())

        hotspot_col.insert_one({
            "cluster_id": int(label),
            "centroid_lat": centroid_lat,
            "centroid_lon": centroid_lon,
            "density_score": round(len(cluster_points) / len(X), 2),
            "updated_at": datetime.utcnow()
        })

    print("✅ Hotspots recomputed successfully")
