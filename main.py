import requests


# This is used to covert the user_input into Latitude and Longituide
def find_geo():
    while True:
        try:
            loc = input("Where you want to go:\n")
            city = input("Specifi The city: ")
            search_loc = loc+", "+city
            print(search_loc)
            request_url = "https://nominatim.openstreetmap.org/search?q=" + search_loc
            params = {"format": "json", "limit": 1}

            headers = {"User-Agent": "Raahi"}

            response = requests.get(
                request_url,
                params=params,
                headers=headers
            )

            data = response.json()
            lat = data[0]["lat"]
            lon = data[0]["lon"]
        except (IndexError,requests.exceptions.ConnectionError):
            print("Nothing Found With such name.")
            pass
        else:
            return lat, lon
        
lat, long = find_geo()
print(lat, long)
