FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

ENV BASE_DIR=/usr/src
ENV APP_DIR=$BASE_DIR/app

WORKDIR $APP_DIR

RUN apt update -y
RUN apt install libpq-dev python3-dev gcc -y
RUN pip install --upgrade pip
COPY requirements.txt $BASE_DIR

RUN pip install -r $BASE_DIR/requirements.txt
COPY . $BASE_DIR

EXPOSE 8000
