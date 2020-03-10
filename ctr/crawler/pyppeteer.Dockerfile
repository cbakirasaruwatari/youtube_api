ARG VERSION=3.8.1-alpine
FROM python:${VERSION} AS python

RUN apk --update add tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*

USER root

RUN pip install \
    'pyppeteer==0.0.25' 
