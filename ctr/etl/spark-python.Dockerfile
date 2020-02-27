# FROM openjdk:8 as spark_build
# ENV SPARK_VERSION=2.4.5
# ENV HADOOP_VERSION=2.7

# USER root
# RUN wget -q http://apache.mirror.iphh.net/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
#     && tar xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
#     && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /spark \
#     && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz


FROM openjdk:8-jre-alpine
ENV PYTHON_VERSION=3.8.1

USER root

# https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.19/mysql-connector-java-8.0.19.jar

RUN apk --update --no-cache add --virtual .build-deps openssl gcc g++ make zlib-dev curl

RUN apk --update --no-cache add python3 python3-dev

RUN pip3 install \
    'oauth2client' \
    'mysql-connector-python==8.0.19' \
    'pyspark==2.4.5' \
    'boto3==1.12.7' \
    'pandas==1.0.1'


RUN apk del .build-deps

EXPOSE 8080