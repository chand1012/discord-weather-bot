# DiscordWeatherBot

![Docker Image](https://github.com/chand1012/discord-weather-bot/workflows/Docker%20Image%20CI/badge.svg?branch=master)

A Discord Bot that gets the weather and COVID-19 country statistics. 

## To use

- For weather data, use the command `!weather`:
    - Use `!weather current <location>` to get the current weather forecast at that location.
    - Use `!weather forecast <location>` to get the forecast for the next 5 to 7 days.
    - Use `!weatherbot counter` to check what the global weather counter is at. If this exceeds 1000, the requests must be stopped until midnight the next day.
    - Examples:
        - `!weather current Akron, Ohio`
        - `!weather current London, England`
        - `!weather forecast Moscow, Russia`
        - `!weather forecast Rhode Island`
- For COVID-19 data, use the command `!covid <country>`. If you wish to look up statistics for US States, you can use the State's two letter postal code, ie. `NY` for New York or `OH` for Ohio, to look up its respective data. If no country or state is selected, the command will display global statistics.
    - Examples:
        - `!covid Germany`
        - `!covid Japan`
        - `!covid USA`
        - `!covid`
        - `!covid WY`

## Add to Server

Coming soon.

## API Info For Geeks

- Uses the [US Weather API](https://www.weather.gov/documentation/services-web-api) (from NOAA).
- Uses [OpenWeatherMap](https://openweathermap.org/) for non US weather data <sub>(there is a limit at the moment)</sub>.
- Uses [Google Maps API](https://cloud.google.com/maps-platform/) for Geo Data.
- Uses [COVIDTracking](https://covidtracking.com/) for US State data.
- Uses [COVID19API](https://covid19api.com/) for all other COVID-related requests.
