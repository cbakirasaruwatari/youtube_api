ARG VERSION=3.8.1-alpine
FROM python:${VERSION} AS python

# additional package for pip
RUN pip install \
    'scrapy' 