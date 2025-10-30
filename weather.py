import requests


weather_code_map = {
    0: "Bezchmurnie ☀️",
    1: "Głównie bezchmurnie 🌤️",
    2: "Częściowe zachmurzenie ⛅",
    3: "Pochmurno ☁️",
    45: "Mgła 🌫️",
    48: "Mgła osadzająca szadź 🌫️❄️",
    51: "Lekka mżawka 🌦️",
    53: "Umiarkowana mżawka 🌦️",
    55: "Gęsta mżawka 🌧️",
    56: "Lekka marznąca mżawka 🌧️❄️",
    57: "Gęsta marznąca mżawka 🌧️❄️",
    61: "Lekki deszcz 🌦️",
    63: "Umiarkowany deszcz 🌧️",
    65: "Ulewny deszcz ⛈️",
    66: "Lekki marznący deszcz 🌧️❄️",
    67: "Ulewny marznący deszcz 🌧️❄️",
    71: "Lekki śnieg ❄️",
    73: "Umiarkowany śnieg ❄️",
    75: "Intensywny śnieg 🌨️",
    77: "Ziarnisty śnieg ❄️",
    80: "Lekkie przelotne opady deszczu 🌦️",
    81: "Umiarkowane przelotne opady deszczu 🌧️",
    82: "Ulewny przelotny deszcz ⛈️",
    85: "Lekkie przelotne opady śniegu 🌨️",
    86: "Ulewny przelotny opad śniegu 🌨️",
    95: "Burza ⛈️",
    96: "Burza z lekkim gradem ⛈️❄️",
    99: "Burza z silnym gradem ⛈️❄️"
}


def geocode_city(city_name):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "pl",
        "format": "json"
    }

    response = requests.get(geo_url, params=params)
    data = response.json()

    if "results" not in data or not data["results"]:
        return None

    result = data["results"][0]
    return {
        "name": result["name"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "country": result.get("country", "")
    }


def get_weather(city_name):
    location = geocode_city(city_name)
    if not location:
        return f"❌ Nie znaleziono miasta: {city_name}"

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": [
        "temperature_2m",
        "apparent_temperature",
        "precipitation",
        "precipitation_probability",
        "weather_code"
        ],
        "timezone": "auto",
        "forecast_days": 2,
        "forecast_hours": 13,
    }

    response = requests.get(url, params=params)
    data = response.json()

    current_data = data['current']

    #current_time_obj = datetime.fromisoformat(current_data['time'])

    result = (
        f"🌤️ Prognoza dla {location['name']}, {location['country']} na godzinę {current_data['time'].split('T')[1]}:\n"
        f"- Temperatura: {current_data['temperature_2m']}°C\n"
        f"- Temperatura odczuwalna: {current_data['apparent_temperature']}°C\n"
        f"- Szansa opadów: {current_data['precipitation_probability']}%\n"
        f"- Ilość opadów: {current_data['precipitation']}mm\n"
        f"- Kod pogody: {weather_code_map.get(current_data['weather_code'])}\n"
    )
       
    return result

def get_forecast(city_name):
    location = geocode_city(city_name)
    if not location:
        return f"❌ Nie znaleziono miasta: {city_name}"

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "hourly": [
        "temperature_2m",
        "apparent_temperature",
        "precipitation",
        "precipitation_probability",
        "weather_code"
        ],
        "timezone": "auto",
        "forecast_days": 2,
        "forecast_hours": 13,
    }

    response = requests.get(url, params=params)
    data = response.json()

    hourly_data = data['hourly']

    #current_time_obj = datetime.fromisoformat(current_data['time'])

    result = (
        f"🌤️ Prognoza dla {location['name']}, {location['country']} na następne 12 godzin:\n\n"
    )
    
    
    for i in range(1, 13):
            result += f"{hourly_data['time'][i].split('T')[1]} - Temperatura: {hourly_data['temperature_2m'][i]}°C, Temperatura odczuwalna: {hourly_data['apparent_temperature'][i]}°C,\
            Szansa opadów: {hourly_data['precipitation_probability'][i]}%, Ilość opadów: {hourly_data['precipitation'][i]}mm,\
            Warunki: {weather_code_map.get(hourly_data['weather_code'][i])}\n"

    return result