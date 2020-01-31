FROM python:3.7-alpine3.10

LABEL maintainer="Yoshimura Yuu <yyu [at] mental.poker>"

WORKDIR /workdir

RUN apk add --no-cache --virtual .qulacs-build-deps \
    cmake \
    make \
    git \
    gcc \
    g++ \
    wget

COPY requirements.txt /workdir/requirements.txt

RUN pip install -r requirements.txt

RUN apk add --no-cache bash

ENTRYPOINT ["/bin/bash", "-c", "flask run --port $PORT --host 0.0.0.0"]