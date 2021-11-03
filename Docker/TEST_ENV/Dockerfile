FROM python:3.7.12

WORKDIR /code

COPY ./requirements.txt .
COPY ./trueLove.pth  /usr/local/lib/python3.7/site-packages

RUN pip install -r requirements.txt

COPY src/ .
 
CMD ["/bin/bash"]