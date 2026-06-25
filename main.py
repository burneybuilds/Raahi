import requests as r
from datetime import date, timedelta

# This is used to covert the user_input into Latitude and Longituide
def find_geo():
    while True:
        try:
            loc = input("Where you want to go: ")
            city = input("Specifi The city: ")
            search_loc = loc+", "+city
            # print(search_loc)
            request_url = "https://nominatim.openstreetmap.org/search?q=" + search_loc
            params = {"format": "json", "limit": 1}

            headers = {"User-Agent": "Raahi"}

            data = r.get(
                request_url,
                params=params,
                headers=headers
            ).json()

            lat = data[0]["lat"]
            lon = data[0]["lon"]
        except (IndexError , r.exceptions.ConnectionError):
            print("Nothing Found With such name.")
            pass
        else:
            return lat, lon
        
def get_weather():
    lat, lon = find_geo()
    weather_points = {
    0: 0,    # Clear sky
    1: 2,    # Mainly clear
    2: 5,    # Partly cloudy
    3: 8,    # Overcast
    61: 12,  # Light rain
    63: 18,  # Moderate rain
    65: 25,  # Heavy rain
    95: 30,  # Thunderstorm
    96: 35,  # Thunderstorm with hail
    99: 40   # Severe thunderstorm
    }
    s_date = date.today()
    e_date = s_date - timedelta(days=7)
    
    current_weather = r.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code")
    future_weather = r.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,weather_code,precipitation_probability")
    past_weather = r.get(f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={e_date}&end_date={s_date}&daily=rain_sum")
    
    if current_weather.status_code == 200:
        current_weather_data = current_weather.json()
        future_weather_data = future_weather.json()
        past_weather_data = past_weather.json()
        past = past_weather_data["daily"]["rain_sum"]
        next5 = future_weather_data["hourly"]["precipitation_probability"][:5]
        code = current_weather_data["current"]["weather_code"]
        total =0
        points =0
        points = weather_points.get(code, 0)
        for i in next5:
            total += i
        avg = total / len(next5)
        score = points + avg
        
        return score


def calculate():
    score = get_weather()
    if score >= 90:
        print("Heavy rain likely")
    elif score >= 70:
        print("Rain likely")
    elif score >= 40:
        print("Chance of rain")
    else:
        print("No rain expected")

calculate()