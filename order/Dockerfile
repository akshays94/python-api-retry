FROM python:3.9

USER root

RUN apt-get update \
  && apt-get -y install \
  build-essential \
  libpq-dev \
  gcc \
  libpng-dev \
  zlib1g-dev \
  libjpeg-dev \
  --no-install-recommends \
  && apt-get clean

RUN pip3 install --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY . .
