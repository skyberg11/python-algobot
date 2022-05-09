FROM ubuntu:latest
RUN mkdir -p usr/src/algobot
WORKDIR /usr/src/algobot
RUN apt-get update 

FROM python:3.8
RUN pip install -U pip && pip install bs4 && pip install telebot 
RUN pip install requests && pip install pyTelegramBotApi && pip install requests-html
COPY . .

ENTRYPOINT [ "python3", "main.py" ]