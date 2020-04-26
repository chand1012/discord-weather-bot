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