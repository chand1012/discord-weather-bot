import logging
import os
import time
from datetime import datetime, timedelta, time

import discord

from covid import CovidCountryData, CovidUSData
from lib import (STATECODES, STATES, all_upper, generate_covid_message,
                 get_7_day_forecast, get_short_forecast, safe_list_get,
                 safe_rest_of_list)
from mapsearch import MapSearch
from weather import USGovWeatherSearch, WeatherSearch

TOKEN = os.environ.get("DISCORDTOKEN")
GOOGLECLOUD = os.environ.get("GOOGLECLOUD")
WEATHERKEY = os.environ.get("WEATHERKEY")

reset = datetime.combine(datetime.now().date(), time(0, 0)) + timedelta(1)
counter = 0
logger = None

def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
     
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error.log"),"w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)

initialize_logger('.')

client = discord.Client()

@client.event
async def on_message(message):
    gmap = MapSearch(key=GOOGLECLOUD)
    if message.author.bot or message.author == client.user:
        return
    if message.content.startswith('!weather'):
        logging.info(f"Request from {message.author.name}: {message.content}")
        split_command = message.content.split(' ')
        second_command = safe_list_get(split_command, 1)
        location = ' '.join(safe_rest_of_list(split_command, 2))

        if time.time() >= reset.timestamp():
            reset = datetime.combine(datetime.now().date(), time(0, 0)) + timedelta(1)
            counter = 0

        if not any(item in message.content for item in ['forecast', 'now', 'current']):
            await message.channel.send(content="Incorrect command Syntax.")
            return

        if second_command is None or location is None:
            await message.channel.send(content="Incorrect command Syntax.")
            return
            
        lat, lng = gmap.get_coordinates(location)
        weather = None

        if gmap.is_us:
            weather = USGovWeatherSearch()
        else:
            if counter<1000: # this will change if I ever get a paid openweathermap membership.
                weather = WeatherSearch(key=WEATHERKEY)
                counter += 1
            else:
                await message.channel.send(content="Sorry for the inconvience, but the global weather request limit has been reached. This will be reset tonight at midnight EST.")
                return
            
        weather.search(lat, lng)
        if 'now' in second_command or 'current' in second_command:
            logging.info("Sending current weather...")
            await message.channel.send(content=get_short_forecast(weather.forecasts))
        elif 'forecast' in second_command:
            logging.info("Sending forecast...")
            for forecast in get_7_day_forecast(weather.forecasts):
                await message.channel.send(content=forecast)
        else:
            await message.channel.send(content='Incorrect command syntax.')

    if message.content.startswith('!covid'):
        logging.info(f"Request from {message.author.name}: {message.content}")
        split_command = message.content.split(' ')
        location = ' '.join(safe_rest_of_list(split_command, 1))
        state_codes = STATECODES.keys()
        covid = None
        test = None
        if location.upper() in STATES or location.upper() in state_codes or 'USA' in location.upper():
            if 'USA' in location.upper():
                location = ''
            covid = CovidUSData()
            test = covid.get_data(state=location)
        elif 'global' in location.lower() or 'globe' in location.lower() or location is '' or location is None:
            covid = CovidCountryData()
            test = covid.get_data()
        else:
            covid = CovidCountryData()
            test = covid.get_data(country=location)
        
        msg = generate_covid_message(covid, location)

        if msg is '':
            logging.error("There was an error. Here is some debug info:")
            logging.error(location.upper())
            logging.error(test)
            await message.channel.send(content="Error! Country not found in COVID-19 Statistics.")
        else:
            logging.info("Sending COVID-19 data....")
            await message.channel.send(content=msg)

    if message.content.startswith('!weatherbot'):
        logging.info(f"Request from {message.author.name}: {message.content}")
        split_command = message.content.split(' ')
        second_command = safe_list_get(split_command, 1)
        if 'counter' in second_command:
            timestring = reset.strftime("%m/%d/%Y, %H:%M:%S")
            await message.channel.send(content=f"The counter is currently at {counter} and will reset at {timestring}.")
        else:
            await message.channel.send(content="Hello from WeatherBot!")

    logging.info('Done.')
    return

@client.event
async def on_ready():
	logging.info('Logged in as')
	logging.info(client.user.name)
	logging.info(client.user.id)
	logging.info('------')

client.run(TOKEN)
