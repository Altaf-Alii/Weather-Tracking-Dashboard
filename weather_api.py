"""
weather_api.py
--------------
Handles all communication with the OpenWeatherMap API.
Keeping this in its own module makes the code modular:
if tomorrow you switch to a different weather API, you
only need to change this file.
"""

import requests


class WeatherAPIError(Exception):
    """Custom exception for all weather-API related errors."""
    pass


class WeatherAPI:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_weather(self, city: str) -> dict:
        """
        Fetch current weather for a given city.
        Raises WeatherAPIError on any problem (bad city, no internet, bad key).
        """
        if not city or not city.strip():
            raise WeatherAPIError("City name cannot be empty.")

        params = {
            "q": city.strip(),
            "appid": self.api_key,
            "units": "metric",  # Celsius
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("No internet connection. Please check your network.")
        except requests.exceptions.Timeout:
            raise WeatherAPIError("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Unexpected network error: {e}")

        if response.status_code == 404:
            raise WeatherAPIError(f"City '{city}' not found. Please check the spelling.")
        if response.status_code == 401:
            raise WeatherAPIError("Invalid API key. Check your .env file.")
        if response.status_code != 200:
            raise WeatherAPIError(f"API returned an error (status {response.status_code}).")

        data = response.json()

        return {
            "city": data.get("name", city),
            "country": data.get("sys", {}).get("country", ""),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        }
