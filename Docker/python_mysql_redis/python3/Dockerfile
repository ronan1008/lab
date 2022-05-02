FROM python:3.9-bullseye
RUN apt-get update \
    && apt-get install -y python3 python3-pip default-mysql-client python3-dev build-essential libssl-dev libffi-dev libgl1-mesa-glx libglib2.0-0 \
    && apt-get install -y redis-tools mariadb-client  # db tools \
    && pip3 install --upgrade pip && apt-get purge -y --auto-remove \
    && apt-get install -y wget
# install python modules
COPY requirements.txt /root/
RUN pip3 install -r /root/requirements.txt

