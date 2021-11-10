FROM ubuntu:20.04
WORKDIR /code

RUN apt-get update \
    && apt-get install -y python3 python3-pip mysql-client python3-dev build-essential libssl-dev libffi-dev libgl1-mesa-glx \
    && pip3 install --upgrade pip && apt-get purge -y --auto-remove

COPY ./requirements.txt .
COPY ./trueLove.pth  /root/.local/lib/python3.8/site-packages/

RUN pip3 install -r requirements.txt

COPY src/ .
