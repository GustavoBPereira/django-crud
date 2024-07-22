FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

ENV BASE_DIR=/usr/src
ENV APP_DIR=$BASE_DIR/app
ENV PYTHONPATH=$BASE_DIR

WORKDIR $APP_DIR

RUN mkdir $BASE_DIR/scripts
COPY requirements.txt $BASE_DIR
COPY ./scripts /scripts

RUN apt update -y
RUN apt install libpq-dev python3-dev gcc -y
RUN pip install --upgrade pip

RUN adduser --disabled-password --no-create-home app && \
    chmod -R +x /scripts

ENV PATH="$PATH:/scripts"

RUN pip install -r $BASE_DIR/requirements.txt
COPY . $BASE_DIR

EXPOSE 8000
USER app

CMD ["run.sh"]