FROM python:3.10.11-alpine3.16 as base

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache bash


RUN apk update \
    && pip install --upgrade pip  


COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["/bin/bash"]






