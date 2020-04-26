from mapquest import MapSearch
from weather import USGovWeatherSearch as WeatherSearch

mapquest = MapSearch()
weather = WeatherSearch()

mapquest.import_keys_from_json()
lat, lng = mapquest.get_coordinates("Atwater, Ohio")

weather.search(lat, lng)
print(weather.forecasts)