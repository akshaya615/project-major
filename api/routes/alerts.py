from fastapi import APIRouter, HTTPException, Header, Depends
from api.core.database import alert_col, hotspot_col
from api.core.security import verify_token
from datetime import datetime
import math

router = APIRouter(tags=["Alerts"])

SEVERITY_THRESHOLD = 7

# =================================================
# JWT AUTH DEPENDENCY
# =================================================
def require_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


# =================================================
# HELPER: Distance calculation (Haversine)
# =================================================
def distance_in_meters(lat1, lon1, lat2, lon2):
    R = 6371000  # meters

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# =================================================
# CREATE ALERT (Severity-based)
# =================================================
@router.post("/")
def create_alert(
    message: str,
    severity: int,
    latitude: float,
    longitude: float
):
    alert = {
        "message": message,
        "severity": severity,
        "latitude": latitude,
        "longitude": longitude,
        "acknowledged": False,
        "created_at": datetime.utcnow()
    }

    if severity >= SEVERITY_THRESHOLD:
        alert_col.insert_one(alert)
        return {"status": "alert_created", "alert": alert}

    return {"status": "no_alert_generated"}


# =================================================
# FETCH ALERTS (JWT PROTECTED)
# =================================================
@router.get("/")
def get_alerts(user=Depends(require_token)):
    alerts = list(alert_col.find({}, {"_id": 0}))
    return {
        "count": len(alerts),
        "alerts": alerts
    }


# =================================================
# ACKNOWLEDGE ALERT (JWT PROTECTED)
# =================================================
@router.post("/ack")
def acknowledge_alert(
    latitude: float,
    longitude: float,
    user=Depends(require_token)
):
    result = alert_col.update_one(
        {"latitude": latitude, "longitude": longitude},
        {"$set": {"acknowledged": True, "ack_time": datetime.utcnow()}}
    )

    if result.modified_count == 1:
        return {"status": "alert_acknowledged"}

    return {"status": "alert_not_found"}


# =================================================
# 🔊 MULTI-LEVEL VOICE HOTSPOT WARNING
# =================================================
@router.get("/voice-warning")
def voice_warning(lat: float, lon: float):

    hotspots = list(hotspot_col.find({}, {"_id": 0}))
    closest_distance = None

    for h in hotspots:
        if h.get("centroid_lat") is None or h.get("centroid_lon") is None:
            continue

        dist = distance_in_meters(
            lat,
            lon,
            h["centroid_lat"],
            h["centroid_lon"]
        )

        if closest_distance is None or dist < closest_distance:
            closest_distance = dist

    # -------------------------------
    # ANNOUNCEMENT LEVELS
    # -------------------------------
    if closest_distance is not None:

        if closest_distance <= 100:
            return {
                "speak": True,
                "message": "Danger! Immediate caution required",
                "distance": int(closest_distance)
            }

        elif closest_distance <= 300:
            return {
                "speak": True,
                "message": "High risk zone ahead, slow down",
                "distance": int(closest_distance)
            }

        elif closest_distance <= 600:
            return {
                "speak": True,
                "message": "Warning! Accident hotspot ahead within 600 meters",
                "distance": int(closest_distance)
            }

    return {"speak": False}
