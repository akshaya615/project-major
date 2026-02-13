import os
import requests

# Load TomTom API key from .env
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")


def get_live_traffic(lat: float, lon: float):
    """
    Returns a normalized traffic congestion score:
    0.0 = free road
    1.0 = heavy traffic

    Uses TomTom Traffic Flow API (free tier)
    """

    # Fallback if API key not found
    if not TOMTOM_API_KEY:
        return 0.3

    try:
        url = (
            "https://api.tomtom.com/traffic/services/4/flowSegmentData/json"
            f"?point={lat},{lon}"
            f"&key={TOMTOM_API_KEY}"
        )

        response = requests.get(url, timeout=5)
        data = response.json()

        flow = data.get("flowSegmentData", {})

        free_flow_speed = flow.get("freeFlowSpeed", 0)
        current_speed = flow.get("currentSpeed", 0)

        # Calculate congestion ratio
        if free_flow_speed > 0:
            congestion = 1 - (current_speed / free_flow_speed)
            return max(0.0, min(1.0, congestion))

        return 0.3

    except Exception:
        # Safe fallback on API failure
        return 0.3
