ARG VERSION=3.8.1-alpine
FROM python:${VERSION} AS python

RUN apk --update add tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*

# additional package for pip
RUN pip install \
    'google-api-python-client' \
    'oauth2client' \
    'mysql-connector-python==8.0.19'
