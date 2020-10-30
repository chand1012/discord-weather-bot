import requests
from datetime import datetime, timedelta
from strings import time_of_day, deg_to_dir


class WorkerWeatherSearch():
    # this uses my Cloudflare worker that reduces the
    # number of requests I have to make on my slow internet
    # it is just middleware for the US government search.
    def __init__(self):
        self.lat = 41.08
        self.lng = -81.51
        self.base_url = "https://weather-api.chand1012.workers.dev"
        self.json = None
        self.forecasts = []

    def search(self, lat, lng):
        self.lat = lat
        self.lng = lng
        req = requests.post(self.base_url, headers={
                            'content-type': 'application/json'}, json={'lat': lat, 'lng': lng})
        self.json = req.json()
        self.forecasts = self.json['properties']['periods']
        return self.json


class USGovWeatherSearch():
    def __init__(self):
        self.lat = 41.08
        self.lng = -81.51
        self.gridx = 0
        self.gridy = 0
        self.base_url = "https://api.weather.gov/"
        self.json = None
        self.url = self.base_url
        self.forecast_url = None
        self.forecasts = []

    def get_points(self):
        self.url = self.base_url + f"/points/{self.lat},{self.lng}"
        req = requests.get(self.url)
        self.json = req.json()
        self.gridx = self.json['properties']['gridX']
        self.gridy = self.json['properties']['gridY']
        self.forecast_url = self.json['properties']['forecast']

    def search(self, lat, lng):
        self.lat = lat
        self.lng = lng
        self.get_points()
        req = requests.get(self.forecast_url)
        self.json = req.json()
        self.forecasts = self.json['properties']['periods']
        return self.forecasts


class WeatherSearch():
    def __init__(self, key=""):
        if not key:
            raise AssertionError("No API key specified!")

        self.key = key
        self.lat = 50
        self.lng = -86
        self.kind = ''
        self.base_url = "http://api.openweathermap.org/"
        self.json = None
        self.url = self.base_url
        self.forecasts = None

    def raw_search(self, lat=None, lng=None, kind="forecast"):
        if lat:
            self.lat = lat
        if lng:
            self.lng = lng

        self.url = f"{self.base_url}data/2.5/{kind}?lat={lat}&lon={lng}&units=metric&appid={self.key}"

        req = requests.get(self.url)
        self.json = req.json()

        return self.json

    def format_json(self):
        firstdate = None
        self.forecasts = []
        for item in self.json['list']:
            data = {}
            date = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
            if firstdate is None:
                firstdate = date
            else:
                firstdate += timedelta(hours=12)
            if date == firstdate:
                aprox = time_of_day(date)
                data['temperatureUnit'] = 'C'
                data['temperature'] = round(item['main']['temp'])
                wind = f'Winds {deg_to_dir(item["wind"]["deg"])} around {round(item["wind"]["speed"])} m/s'
                if item["wind"].get("gust"):
                    wind += f' with gusts of up to {item["wind"]["gust"]} m/s'
                data['detailedForecast'] = f'{item["weather"][0]["description"].capitalize()} with a high temperature near {round(item["main"]["temp_max"])}C, low of {round(item["main"]["temp_min"])}C. {wind}'
                data['name'] = item['dt_txt']
                if aprox == "night":
                    data['name'] = "Tonight"
                if aprox == "morning":
                    data['name'] = "This Morning"
                if aprox == "afternoon":
                    data['name'] = "This Afternoon"
                if aprox == "evening":
                    data['name'] = "This Evening"
                self.forecasts += [data]

    def search(self, lat=None, lng=None, kind="forecast"):
        self.raw_search(lat, lng, kind)
        self.format_json()
        return self.forecasts
