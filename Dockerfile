FROM python:3.6.10-alpine
LABEL org.opencontainers.image.source=https://github.com/chand1012/discord-weather-bot
COPY . /app
WORKDIR /app
RUN apk add --update build-base
RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt
CMD python ./bot.py
