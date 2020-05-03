def get_short_forecast(forecast_list):
    forecast = forecast_list[0]
    return_string = forecast['name'] + '\n'
    return_string += f'Temperature: {forecast["temperature"]}{forecast["temperatureUnit"]}\n'
    return_string += forecast['detailedForecast']
    return return_string

def get_7_day_forecast(forecast_list):
    return_list = []
    for forecast in forecast_list:
        return_string = forecast['name'] + '\n'
        return_string += f'Temperature: {forecast["temperature"]}{forecast["temperatureUnit"]}\n'
        return_string += forecast['detailedForecast'] + '\n'
        return_string += '-' * 20
        return_list += [return_string]
    return return_list

def time_of_day(date):
    hours = list(range(24))
    if int(date.hour) in hours[20:] or int(date.hour) in hours[:4]:
        return "night"
    elif int(date.hour) in hours[5:12]:
        return "morning"
    elif int(date.hour) in hours[13:17]:
        return "afternoon"
    else:
        return "evening"

def deg_to_dir(direction):
    # http://snowfence.umn.edu/Components/winddirectionanddegrees.htm

    while direction >= 360:
        direction -= 360

    if direction < 11.25 or direction >= 348.75:
        return "N"
    if 11.25 <= direction < 33.75:
        return "NNE"
    if 33.75 <= direction < 56.25:
        return "NE"
    if 56.25 <= direction < 78.75:
        return "ENE"
    if 78.75 <= direction < 101.25:
        return "E"
    if 101.25 <= direction < 123.75:
        return "ESE"
    if 123.75 <= direction < 146.25:
        return "SE"
    if 146.25 <= direction < 168.75:
        return "SSE"
    if 168.75 <= direction < 191.25:
        return "S"
    if 191.25 <= direction < 213.75:
        return "SSW"
    if 213.75 <= direction < 236.25:
        return "SW"
    if 236.25 <= direction < 258.75:
        return "WSW"
    if 258.75 <= direction < 281.25:
        return "W"
    if 281.25 <= direction < 303.75:
        return "NW"
    if 326.25 <= direction < 348.75:
        return "NNW"
    
def safe_list_get(item, index, default=None):
    try:
        return item[index]
    except IndexError:
        return default

def safe_rest_of_list(item, index, default=None):
    try:
        return item[index:]
    except IndexError:
        return default

def find_item_by_attr(list_dict, attr, search):
    for item in list_dict:
        if item[attr] == search:
            return item