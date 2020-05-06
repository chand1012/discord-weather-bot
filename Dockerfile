FROM python:3.6.10-alpine
COPY . /app
WORKDIR /app
RUN apk add --update build-base
RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt
CMD python ./bot.py
