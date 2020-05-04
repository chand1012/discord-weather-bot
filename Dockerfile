FROM python:alpine3.6
COPY . /app
WORKDIR /app
RUN apk add --update build-base
RUN pip install -r requirements.txt
CMD python ./bot.py
