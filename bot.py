import logging
import os
import time
from datetime import datetime

import discord

from covid import CovidCountryData, CovidUSData
from lib import (STATECODES, STATES, get_counter, get_time, increment_counter,
                 set_counter, set_time)
from list_dict import find_item_by_attr, safe_list_get, safe_rest_of_list
from mapsearch import MapSearch
from strings import (deg_to_dir, generate_covid_message, get_7_day_forecast,
                     get_short_forecast, time_of_day)
from weather import WeatherSearch, USGovWeatherSearch
#from weather import WorkerWeatherSearch as USGovWeatherSearch
from topgg import update_server_count

TOKEN = os.environ.get("DISCORDTOKEN")
GOOGLECLOUD = os.environ.get("GOOGLECLOUD")
WEATHERKEY = os.environ.get("WEATHERKEY")
TOPGG = os.environ.get("TOPGG")

set_time()
set_counter()
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
    if message.author.bot or message.author == client.user:
        return

    if message.content.startswith('!weatherbot'):
        logging.info(f"Request: {message.content}")
        split_command = message.content.split(' ')
        second_command = safe_list_get(split_command, 1)
        if 'counter' in second_command:
            counter = get_counter()
            timestring = datetime.fromtimestamp(get_time()).strftime("%m/%d/%Y, %H:%M:%S")
            msg = f"The counter is currently at {counter} and will reset at {timestring}."
            logging.info(msg)
            await message.channel.send(content=msg)
        else:
            await message.channel.send(content="Hello from WeatherBot!")

    elif message.content.startswith('!weather'):
        gmap = MapSearch(key=GOOGLECLOUD)
        counter = get_counter()
        logging.info(f"Request: {message.content}")
        logging.info("Parsing command...")
        split_command = message.content.split(' ')
        second_command = safe_list_get(split_command, 1)
        location = ' '.join(safe_rest_of_list(split_command, 2))

        if time.time() >= get_time():
            set_time()
            set_counter()

        if not any(item in message.content for item in ['forecast', 'now', 'current']):
            await message.channel.send(content="Incorrect command Syntax.")
            return

        if second_command is None or location is None:
            await message.channel.send(content="Incorrect command Syntax.")
            return
        
        logging.info("Getting coordinates of location...")
        lat, lng = gmap.get_coordinates(location)
        weather = None

        if gmap.is_us:
            logging.info("Using NOAA Weather Data.")
            weather = USGovWeatherSearch()
        else:
            if counter<1000: # this will change if I ever get a paid openweathermap membership.
                logging.info("Using OpenWeatherMap Data.")
                weather = WeatherSearch(key=WEATHERKEY)
                increment_counter()
            else:
                logging.warning("Counter has reached 1000, cannot use OpenWeatherMap until tomorrow.")
                await message.channel.send(content="Sorry for the inconvience, but the global weather request limit has been reached. This will be reset tonight at midnight EST.")
                return
        try:
            weather.search(lat, lng)
        except Exception as e:
            logging.error(e)
            logging.error(f"Given location: {location}")
            logging.error(f"Lat: {lat}, Lng: {lng}")
            await message.channel.send(content="There was an error processing your request. If this persists, please report it here: https://github.com/chand1012/discord-weather-bot/issues")
            return
        if 'now' in second_command or 'current' in second_command:
            logging.info("Sending current weather...")
            await message.channel.send(content=get_short_forecast(weather.forecasts))
        elif 'forecast' in second_command:
            logging.info("Sending forecast...")
            for forecast in get_7_day_forecast(weather.forecasts):
                await message.channel.send(content=forecast)
        else:
            await message.channel.send(content='Incorrect command syntax.')

    elif message.content.startswith('!covid'):
        logging.info(f"Request: {message.content}")
        split_command = message.content.split(' ')
        location = ' '.join(safe_rest_of_list(split_command, 1))
        state_codes = STATECODES.keys()
        covid = None
        test = None
        if location.upper() in STATES or location.upper() in state_codes or 'USA' in location.upper():
            logging.info("Getting COVID-19 data for the US.")
            if 'USA' in location.upper():
                location = ''
            covid = CovidUSData()
            test = covid.get_data(state=location)
        elif 'global' in location.lower() or 'globe' in location.lower() or location is '' or location is None:
            logging.info("Getting global COVID-19 data.")
            covid = CovidCountryData()
            test = covid.get_data()
        else:
            logging.info(f"Getting COVID-19 data for {location}.")
            covid = CovidCountryData()
            test = covid.get_data(country=location)
        
        logging.info("Generating message...")
        msg = generate_covid_message(covid, location)

        if msg is '':
            logging.error("There was an error. Here is some debug info:")
            logging.error(location.upper())
            logging.error(test)
            await message.channel.send(content="Error! Country not found in COVID-19 Statistics.")
        else:
            logging.info("Sending COVID-19 data....")
            await message.channel.send(content=msg)

    if not TOPGG is None:
        update_server_count(TOPGG, client.user.id, len(client.guilds))
    logging.info('Done.')
    return

@client.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(client.user.name)
    logging.info(client.user.id)
    logging.info('------')
    if not TOPGG is None:
        update_server_count(TOPGG, client.user.id, len(client.guilds))

client.run(TOKEN)
