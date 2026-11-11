"""Get the current weather and a 3-day forecast for any city.

Uses the free Open-Meteo APIs (no API key needed):
  1. Geocoding API -> turns a city name into latitude/longitude
  2. Forecast API  -> returns weather for that latitude/longitude
"""

import sys

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Open-Meteo returns a number (WMO weather code). This maps it to text.
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    56: "Freezing drizzle",
    57: "Freezing drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Freezing rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Rain showers",
    81: "Rain showers",
    82: "Heavy rain showers",
    85: "Snow showers",
    86: "Snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with hail",
}


def find_city(name):
    """Return the first matching place for a city name, or None."""
    response = requests.get(GEOCODING_URL, params={"name": name, "count": 1}, timeout=10)
    response.raise_for_status()
    results = response.json().get("results")
    if not results:
        return None
    return results[0]


def get_forecast(latitude, longitude):
    """Return current weather and a 3-day daily forecast."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "timezone": "auto",
        "forecast_days": 3,
    }
    response = requests.get(FORECAST_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def describe(code):
    return WEATHER_CODES.get(code, "Unknown")


def main():
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
    else:
        city = input("Enter a city: ").strip()

    if not city:
        print("Please type a city name.")
        return

    try:
        place = find_city(city)
        if place is None:
            print(f"Could not find '{city}'. Check the spelling and try again.")
            return
        data = get_forecast(place["latitude"], place["longitude"])
    except requests.exceptions.RequestException as error:
        print("Could not reach the weather service:", error)
        return

    now = data["current"]
    location = place["name"]
    if place.get("country"):
        location += ", " + place["country"]
    print(f"\nWeather in {location}")
    print("-" * 35)
    print(f"Now:      {now['temperature_2m']} °C, {describe(now['weather_code'])}")
    print(f"Humidity: {now['relative_humidity_2m']} %")
    print(f"Wind:     {now['wind_speed_10m']} km/h")

    print("\nNext 3 days")
    daily = data["daily"]
    for day, low, high, code in zip(
        daily["time"],
        daily["temperature_2m_min"],
        daily["temperature_2m_max"],
        daily["weather_code"],
    ):
        print(f"{day}:  {low} to {high} °C, {describe(code)}")


if __name__ == "__main__":
    main()
