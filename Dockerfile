FROM python:3.8

RUN apt-get update -y

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app/

ENTRYPOINT [ "python", "/app/main.py" ]

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app