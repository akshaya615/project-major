from fastapi import APIRouter, HTTPException
from api.core.database import hotspot_col, kde_col

router = APIRouter(tags=["Hotspots"])

# -------------------------------------------------
# HDBSCAN HOTSPOTS
# -------------------------------------------------
@router.get("/hdbscan")
def get_hdbscan_hotspots():
    try:
        data = list(hotspot_col.find({}, {"_id": 0}))

        hotspots = []
        for h in data:
            hotspots.append({
                "cluster_id": h.get("cluster_id", -1),
                "centroid_lat": h.get("centroid_lat"),
                "centroid_lon": h.get("centroid_lon"),
                "density_score": h.get("density_score", 0)
            })

        return {
            "count": len(hotspots),
            "hotspots": hotspots
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# KDE HEATMAP (FIXED)
# -------------------------------------------------
@router.get("/kde")
def get_kde_heatmap():
    try:
        data = list(kde_col.find({}, {"_id": 0}))

        heatmap = []

        for p in data:
            # Handle different possible key names safely
            lat = p.get("lat") or p.get("latitude") or p.get("x")
            lng = p.get("lng") or p.get("longitude") or p.get("y")
            intensity = (
                p.get("density")
                or p.get("value")
                or p.get("intensity")
                or 1.0
            )

            # Only add valid points
            if lat is not None and lng is not None:
                heatmap.append({
                    "lat": float(lat),
                    "lng": float(lng),
                    "intensity": float(intensity)
                })

        return {
            "count": len(heatmap),
            "heatmap": heatmap
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
