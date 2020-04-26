import requests
import time
import json

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
        self.forcasts = None

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
        if key is "":
            raise AssertionError("No API key specified!")

        self.key = key
        self.lat = 50
        self.lng = -86
        self.kind = ''
        self.base_url = "http://api.openweathermap.org/"
        self.json = None
        self.formated_json = None
        self.url = self.base_url
        self.forecasts = None

    def raw_search(self, lat=None, lng=None, kind="forecast"):
        if not lat is None:
            self.lat = lat
        if not lng is None:
            self.lng = lng

        query = f"{self.lat},{self.lng}"
        self.url = f"{self.base_url}data/2.5/{kind}?lat={lat}&lon={lng}&units=metric&appid={self.key}"

        req = requests.get(self.url)
        self.json = req.json()
        
        return req.json()

    def format_json(self):
        pass

    def search(self, lat=None, lng=None, kind="forecast"):
        self.raw_search(lat, lng, kind)
        self.format_json()
        return self.formated_json

