FROM python:3.7-slim-buster

ENV SHELL /bin/bash

WORKDIR AR-filter-cpm

RUN apt-get update
RUN apt install build-essential -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install cmake -y

COPY requirements.txt AR-filter-cpm/requirements.txt

RUN pip install -r AR-filter-cpm/requirements.txt

CMD ["tail", "-f", "/dev/null"]