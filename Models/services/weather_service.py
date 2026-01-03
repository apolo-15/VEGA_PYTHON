import requests


CITIES = {
    "sevilla": (37.3886, -5.9823),
    "madrid": (40.4168, -3.7038),
    "malaga": (36.7213, -4.4214),
}


def get_weather(city):
    if city not in CITIES:
        return None

    latitude, longitude = CITIES[city]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&current_weather=true"
    )

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except Exception:
        return None

    if "current_weather" not in data:
        return None

    weather_data = data["current_weather"]

    return [
        f"📍 {city.capitalize()}",
        f"🌡️ {weather_data['temperature']} °C",
        f"💨 {weather_data['windspeed']} km/h",
    ]
