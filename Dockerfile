FROM python:3.8

ENV MICRO_SERVICE=/home/app/microservice

RUN mkdir -p $MICRO_SERVICE

# where the code lives
WORKDIR $MICRO_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . $MICRO_SERVICE
