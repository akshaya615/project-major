# api/services/weather_service.py

import os
import requests

# Load API key from environment (.env)
WEATHER_API_KEY = os.getenv("c21a7e12017ee090a24693125520648e")

def get_live_weather(latitude: float, longitude: float):
    """
    Fetch live weather from OpenWeatherMap API
    Returns rain, visibility, and weather condition code
    """

    # If API key is missing, return safe defaults
    if not WEATHER_API_KEY:
        return {
            "rain": 0.0,
            "visibility": 10000,
            "weather_code": 0
        }

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        # Rain in last 1 hour (mm)
        rain = data.get("rain", {}).get("1h", 0.0)

        # Visibility in meters
        visibility = data.get("visibility", 10000)

        # Weather condition code (OpenWeatherMap)
        weather_code = data.get("weather", [{}])[0].get("id", 0)

        return {
            "rain": float(rain),
            "visibility": int(visibility),
            "weather_code": int(weather_code)
        }

    except Exception as e:
        # Fallback values if API fails
        return {
            "rain": 0.0,
            "visibility": 10000,
            "weather_code": 0
        }
