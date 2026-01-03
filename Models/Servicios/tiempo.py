import requests

CIUDADES = {
    "sevilla": (37.3886, -5.9823),
    "madrid": (40.4168, -3.7038),
    "malaga": (36.7213, -4.4214),
}

def obtener_tiempo(ciudad):
    if ciudad not in CIUDADES:
        return None

    lat, lon = CIUDADES[ciudad]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current_weather=true"
    )

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except Exception:
        return None

    if "current_weather" not in data:
        return None

    clima = data["current_weather"]

    return [
        f"📍 {ciudad.capitalize()}",
        f"🌡️ {clima['temperature']} °C",
        f"💨 {clima['windspeed']} km/h",
    ]
