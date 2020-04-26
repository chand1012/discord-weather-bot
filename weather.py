import requests
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
