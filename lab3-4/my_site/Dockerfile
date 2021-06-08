FROM python:3.8.5-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /lab3

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /lab3/