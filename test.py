import os

from lib import get_short_forecast
from mapquest import MapSearch
from weather import WeatherSearch

mapquest = MapSearch()
weather = WeatherSearch(key=os.environ.get("WEATHERKEY"))

mapquest.import_keys_from_json()
lat, lng = mapquest.get_coordinates("Ontario, Canada")
print(f"Ontario, Canada coordinates: {lat}, {lng}")

print(weather.raw_search(lat, lng))
