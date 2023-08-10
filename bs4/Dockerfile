FROM python:3.11
COPY . /app
WORKDIR /app
RUN apt update
RUN apt upgrade -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt