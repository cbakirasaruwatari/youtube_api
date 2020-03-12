#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import configparser
import mysql.connector as mydb
import boto3
import json
from datetime import datetime

# import pandas as pd
from pyspark.sql import SQLContext, Row
from pyspark import SparkContext
import pandas as pd



class PersitenceDatabaseConnector:
  _CFG_PATH:str = './resource/settings/resource.cfg'
  errors = mydb.errors
  def __init__(
                self,
                resource_name: str,
                resource_name_sub: str
              ):

    if os.path.isfile(self._CFG_PATH) is False:
        raise FileNotFoundError
    cfg = configparser.SafeConfigParser(os.environ)
    cfg.read(self._CFG_PATH)


    self.__host=cfg[resource_name]["db_host"]
    self.__port=cfg[resource_name]["db_port"]
    self.__user=cfg[resource_name + "_" + resource_name_sub]["db_user"]
    self.__password=cfg[resource_name + "_" + resource_name_sub]["db_password"]
    self.__database=cfg[resource_name + "_" + resource_name_sub]["db_database"]

  def connect(self):
    self.conn = mydb.connect(
      host=self.__host,
      port=self.__port,
      user=self.__user,
      password=self.__password,
      database=self.__database
    )
    self.cursor = self.conn.cursor()
  def close(self):
    self.conn.close()
    self.cursor.close()
  def commit(self):
    self.conn.commit()   
  def rollback(self):
    self.conn.rollback()

if __name__ == "__main__":

    youtuber_resource = PersitenceDatabaseConnector("crawler","youtuber")
    try:
        youtuber_resource.connect()
        youtuber_resource.cursor.execute('select url from youtuber')
        urls = [d[0] for d in youtuber_resource.cursor.fetchall()]
    except youtuber_resource.errors.ProgrammingError as e:
        print(e)
        sys.exit()
    finally:
        youtuber_resource.close()

    youtube_resource = PersitenceDatabaseConnector("google_api","youtube")

    youtube_resource.connect()
    for url in urls:
      try:
        youtube_resource.cursor.execute("INSERT INTO channels_resource (url) VALUES (%s)",[url[url.rfind("/")+1:]])
      except youtube_resource.errors.ProgrammingError as e:
        print(e)
        youtube_resource.close()
        sys.exit()
      except youtube_resource.errors.IntegrityError as e:
        continue
    youtube_resource.commit()
    youtube_resource.close()

    