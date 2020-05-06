# This is an open source project
# Feel free to use this when necessary.
# - chand1012

import json

from googlemaps import Client as GClient

from list_dict import safe_list_get


class MapSearch():
    def __init__(self, key=''):
        self.key = key
        self.lat = None
        self.lng = None
        self.country = ''
        self.is_us = False
        self.json = None
        if self.key is '':
            raise AssertionError("There was no API keys specified.")
        self.client = GClient(key=self.key)

    # returns all of the data from the location
    def search_address(self, location="Akron, Ohio"):
        self.json = safe_list_get(self.client.geocode(location), 0)
        components = self.json['address_components']
        for thing in components:
            if 'country' in thing['types']:
                self.country = thing['long_name']
                self.is_us = ('US' in thing['short_name'])
        self.lat = self.json['geometry']['location']['lat']
        self.lng = self.json['geometry']['location']['lng']
        return self.json

    # returns the coordinates
    def get_coordinates(self, location="Kansas City, MO"):
        self.search_address(location)
        return self.lat, self.lng
