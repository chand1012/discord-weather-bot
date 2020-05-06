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

def generate_covid_message(covid_obj, location):
    return_string = ''

    if covid_obj.total is -1 or covid_obj.deaths is -1 or covid_obj.recovered is -1:
        return return_string

    if covid_obj.mode is 'us':
        return_string += "COVID-19 Statistics for the United States:\n"
    elif covid_obj.mode is 'state':
        return_string += f"COVID-19 Statistics for the US State of {covid_obj.state}:\n"
    elif covid_obj.mode is 'country':
        return_string += f"COVID-19 Statistics for {covid_obj.country}:\n"
    elif covid_obj.mode is 'global':
        return_string += "Global COVID-19 Statistics:\n"
    else:
        return_string += f"COVID-19 Statistics for {location}:"
    
    if covid_obj.total is None or covid_obj.total is 0:
        return_string += "There is no data for total confirmed cases in this area.\n"
    else:
        return_string += f"Total Confirmed Cases: {covid_obj.total:,}\n"

    if covid_obj.deaths is None or covid_obj.deaths is 0:
        return_string += "There is no data for total confirmed deaths in this area.\n"
    else:
        return_string += f"Total Confirmed Deaths: {covid_obj.deaths:,}\n"

    if covid_obj.recovered is None or covid_obj.recovered is 0:
        return_string += "There is no data for recovered cases in this area.\n"
    else:
        return_string += f"Total COVID-19 Recoveries: {covid_obj.recovered:,}\n"

    return return_string

def all_lower(list_of_strings):
    final_list = []
    for item in list_of_strings:
        final_list += [item.lower()]
    return final_list

def all_upper(list_of_strings):
    final_list = []
    for item in list_of_strings:
        final_list += [item.upper()]
    return final_list
