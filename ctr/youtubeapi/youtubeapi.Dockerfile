ARG VERSION=3.8.1-alpine
FROM python:${VERSION} AS python

# additional package for pip
RUN pip install \
    'google-api-python-client' \
    'oauth2client' \
    'mysql-connector-python==8.0.19'


WORKDIR /home