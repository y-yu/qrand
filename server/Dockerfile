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

RUN pip install -r requirements.txt && \
    apk del .qulacs-build-deps

ENTRYPOINT ["/bin/bash", "-c", "flask run"]