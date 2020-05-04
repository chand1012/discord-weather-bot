from datetime import datetime, time, timedelta

STATECODES = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

STATES = ['ALABAMA', 'ALASKA', 'AMERICAN SAMOA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO', 'CONNECTICUT', 'DELAWARE', 'DISTRICT OF COLUMBIA', 'FEDERATED STATES OF MICRONESIA', 'FLORIDA', 'GEORGIA', 'GUAM', 'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA', 'MAINE', 'MARSHALL ISLANDS', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'NORTHERN MARIANA ISLANDS', 'OHIO', 'OKLAHOMA', 'OREGON', 'PALAU', 'PENNSYLVANIA', 'PUERTO RICO', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGIN ISLANDS', 'VIRGINIA', 'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']

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

def set_time(filename="time.txt"):
    reset = datetime.combine(datetime.now().date(), time(0, 0)) + timedelta(1)
    with open(filename, 'w') as f:
        f.write(str(reset.timestamp()))

def get_time(filename="time.txt"):
    t = ""
    with open(filename) as f:
        t = f.read()
    return float(t)

def get_counter(filename="counter.txt"):
    t = ""
    with open(filename) as f:
        t = f.read()
    return int(t)

def increment_counter(filename="counter.txt"):
    count = get_counter(filename=filename)+1
    with open(filename, 'w') as f:
        f.write(str(count))

def set_counter(filename="counter.txt", count=0):
    with open(filename, 'w') as f:
        f.write(str(count))