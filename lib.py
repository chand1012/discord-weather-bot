import requests
import json

class MapSearch():
    def __init__(self, key='', secret=''):
        self.key = key
        self.secret = secret
        self.body = None # last json request sent
        self.url = '' # last used url
        self.json = None

    def import_keys_from_json(self, filename="keys.json"):
        data = {}
        with open(filename) as f:
            data = json.loads(f.read())
        self.key = data['key']
        self.secret = data['secret']

    def search_address(self, location="Akron, Ohio"):
        if self.key is '' or self.secret is '':
            raise AssertionError("There was no API keys specified.")

        self.body =  {
            "location":location,
            "options": {
                "thumbMaps": False
            }
        }
        self.url = f"http://open.mapquestapi.com/geocoding/v1/address?key={self.key}"
        req = requests.post(self.url, data=self.body)
        self.json = req.json()
        return self.json

if __name__=='__main__':
    mapquest = MapSearch()
    mapquest.import_keys_from_json()
    print(mapquest.search_address())
        