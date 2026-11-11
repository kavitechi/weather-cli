# Weather CLI

A command-line Python script that shows the current weather and a 3-day forecast for any city. I made it to practise working with REST APIs and JSON.

It uses two free [Open-Meteo](https://open-meteo.com/) APIs, and neither needs an API key:
1. **Geocoding API**: converts the city name into latitude and longitude
2. **Forecast API**: returns the weather for those coordinates

## Run it
```
pip install -r requirements.txt
python weather.py Bengaluru
```
or just `python weather.py` and type the city when asked.

Example output:
```
Weather in Bengaluru, India
-----------------------------------
Now:      23.6 °C, Overcast
Humidity: 47 %
Wind:     8.5 km/h

Next 3 days
2026-11-11:  18.6 to 29.0 °C, Overcast
...
```

## Testing the APIs in Postman
Before writing the code, I tried both endpoints in Postman to understand the request parameters and the JSON response. The collection is in `postman/weather.postman_collection.json`.

## What I learned
- Making GET requests with query parameters using `requests`
- Reading nested JSON responses
- Handling errors: unknown city, no internet, timeouts
- Chaining two APIs, where the output of the first is the input of the second
