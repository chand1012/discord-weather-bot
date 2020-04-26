import os

from weather import WeatherSearch

weather = WeatherSearch(key=os.environ.get("WEATHERKEY"))

weather.raw_search(51.5073, -0.1277, "weather")
print(weather.json)
