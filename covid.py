import requests

class CovidCountryData():
    def __init__(self):
        pass

class CovidStateData():
    def __init__(self, state=""):
        self.state = state.capitalize()
        self.country = False
        if state is "":
            self.country = True
        self.grade = ""
        self.total_cases = -1
        self.recovered = -1
        self.deaths = -1
        self.ventilator = -1
        self.icu_cases = -1
        self.hospitalized = -1
        self.url = ""
        self.state_json = None
        if state is "":
            self.url = "https://covidtracking.com/api/v1/us/current.json"
        else:
            self.url = "https://covidtracking.com/api/v1/states/current.json"
        self.json = None
        
    def get_data(self):
        req = requests.get(self.url)
        if req.status_code != 200:
            raise requests.HTTPError("Returned non-200 code. Please retry or check your syntax.")
        self.json = req.json()

        return self.json()

    
