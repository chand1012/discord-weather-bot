import logging
import os

import discord

from lib import (get_7_day_forecast, get_short_forecast, safe_list_get,
                 safe_rest_of_list)
from mapsearch import MapSearch
from weather import USGovWeatherSearch, WeatherSearch

TOKEN = os.environ.get("DISCORDTOKEN")
GOOGLECLOUD = os.environ.get("GOOGLECLOUD")
WEATHERKEY = os.environ.get("WEATHERKEY")

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

        if second_command is None or location is None:
            await message.channel.send(content="Incorrect command Syntax.")
            
        lat, lng = gmap.get_coordinates(location)
        weather = None

        if gmap.is_us:
            weather = USGovWeatherSearch()
        else:
            weather = WeatherSearch(key=WEATHERKEY)
            
        weather.search(lat, lng)
        if 'now' in second_command or 'current' in second_command:
            await message.channel.send(content=get_short_forecast(weather.forecasts))
        elif 'forecast' in second_command:
            for forecast in get_7_day_forecast(weather.forecasts):
                await message.channel.send(content=forecast)
        else:
            await message.channel.send(content='Incorrect command syntax.')
    return

@client.event
async def on_ready():
	logging.info('Logged in as')
	logging.info(client.user.name)
	logging.info(client.user.id)
	logging.info('------')

client.run(TOKEN)
