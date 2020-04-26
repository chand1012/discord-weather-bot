import logging
import os

import discord

from lib import get_short_forecast, get_7_day_forecast
from mapquest import MapSearch
from weather import USGovWeatherSearch

TOKEN = os.environ.get("DISCORDTOKEN")
MAPQUEST_KEY = os.environ.get("MAPQUESTKEY")
MAPQUEST_SECRET = os.environ.get("MAPQUESTSECRET")

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
    mapquest = MapSearch(MAPQUEST_KEY, MAPQUEST_SECRET)
    weather = None
    if message.content.startswith('!weather'):
        split_command = message.content.split(' ')
        second_command = split_command[1]
        location = split_command[2:]
        lat, lng = mapquest.get_coordinates(location)
        if mapquest.is_us:
            weather = USGovWeatherSearch()
        else:
            # weather = WeatherSearch()
            await message.channel.send(content="I am sorry, but we do not support weather forecasts outside the United States at this time. Please try again at a later date.")
            return
        weather.search(lat, lng)
        if 'now' in second_command:
            await message.channel.send(content=get_short_forecast(weather.forecasts))
        elif 'week' in second_command:
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