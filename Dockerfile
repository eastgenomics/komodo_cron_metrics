FROM python:3.8

RUN apt-get update -y

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir /prom_metrics
WORKDIR /app/

ENTRYPOINT [ "python", "/app/main.py" ]

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app