import requests
from lib import STATECODES

class CovidCountryData():
    def __init__(self):
        self.url = "https://api.covid19api.com/summary"
        self.country_code = ""
        self.country = ""
        self.total = -1
        self.deaths = -1
        self.recovered = -1
        self.json = {}
        self.mode = ""
    
    def get_data(self, country=""):
        req = requests.get(self.url)
        if req.status_code != 200:
            raise requests.HTTPError("Returned non-200 code. Please retry or check your syntax.")
        self.json = req.json()
        if not country:
            globalData = self.json['Global']
            self.total = globalData['TotalConfirmed']
            self.deaths = globalData['TotalDeaths']
            self.recovered = globalData['TotalRecovered']
            self.mode = "global"
        else:
            for item in self.json['Countries']:
                if country.lower() in item['Country'].lower() or country.lower() in item['CountryCode'].lower():
                    self.total = item['TotalConfirmed']
                    self.deaths = item['TotalDeaths']
                    self.recovered = item['TotalRecovered']
                    self.mode = "country"
                    self.country = item['Country']
                    self.country_code = item['CountryCode']
                    break

        return self.total, self.deaths, self.recovered

class CovidUSData():
    def __init__(self):
        self.mode = ""
        self.total = -1
        self.deaths = -1
        self.recovered = -1
        self.url = ""
        self.json = None
        self.state = ""
        self.state_code = ""
        
    def get_data(self, state=""):
        if not state:
            self.url = "https://covidtracking.com/api/v1/us/current.json"
        else:
            self.url = "https://covidtracking.com/api/v1/states/current.json"
        
        req = requests.get(self.url)
        if req.status_code != 200:
            raise requests.HTTPError("Returned non-200 code. Please retry or check your syntax.")
            
        self.json = req.json()

        if not state:
            self.mode = "us"
            self.total = self.json[0]['totalTestResults']
            self.deaths = self.json[0]['death']
            self.recovered = self.json[0]['recovered']
        else:
            stateData = {}
            self.mode = "state"
            self.state_code = state.upper()
            self.state = STATECODES.get(state.upper())
            for item in self.json:
                if self.state_code in item['state']:
                    self.total = item['totalTestResults']
                    self.deaths = item['death']
                    self.recovered = item['recovered']
                    break
            
        return self.total, self.deaths, self.recovered
    
