FROM python:3.10

WORKDIR /app

ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
