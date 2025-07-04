FROM python:3.11-slim

LABEL author=${AUTHOR}
COPY . ./services

WORKDIR /services/ml_service

RUN ["pip3", "install", "-r", "../requirements.txt"]

EXPOSE ${MAIN_PORT}

VOLUME /services/models

CMD uvicorn predict_app:app --reload --port ${MAIN_PORT} --host 0.0.0.0