from json import loads


def json_extract(thing='', filename='discord.json'):
    json_file = open(filename)
    json_data = loads(json_file.read())
    json_file.close()
    if not thing is '':
        return json_data[thing]
    else:
        return json_data

def get_short_forecast(forecast_list):
    forecast = forecast_list[0]
    return_string = forecast['name'] + '\n'
    return_string += f'Temperature: {forecast["temperature"]}{forecast["temperatureUnit"]}\n'
    return_string += forecast['detailedForecast']
    return return_string
