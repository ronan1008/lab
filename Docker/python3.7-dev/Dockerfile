FROM python:3.7.12

WORKDIR /code

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .
 
CMD ["/bin/bash"]