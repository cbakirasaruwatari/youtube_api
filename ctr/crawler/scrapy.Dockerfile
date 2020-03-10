ARG VERSION=3.8.1-alpine
FROM python:${VERSION} AS python

RUN apk --update add tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*

USER root

RUN apk add --update --no-cache  --virtual .build-deps \
    build-base \
    python-dev \
    zlib-dev 


RUN apk add --update --no-cache \
    libxml2-dev \
    libxslt-dev \
    openssl-dev \
    libffi-dev

# additional package for pip
RUN pip install \
    'Scrapy==2.0.0' 

RUN apk del .build-deps