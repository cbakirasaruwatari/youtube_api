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
                db_name: str
              ):

    if os.path.isfile(self._CFG_PATH) is False:
        raise FileNotFoundError
    cfg = configparser.SafeConfigParser(os.environ)
    cfg.read(self._CFG_PATH)

    self.__host=cfg["youtube_db"]["db_host"]
    self.__port=cfg["youtube_db"]["db_port"]
    self.__user=cfg["youtube_db_" + db_name]["db_user"]
    self.__password=cfg["youtube_db_" + db_name]["db_password"]
    self.__database=cfg["youtube_db_" + db_name]["db_database"]

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
    column_neames = {
        "id":"チャンネルID",
        "snippet.title":"チャンネルタイトル",
        "snippet.description":"チャンネル説明",
        "snippet.publishedAt":"チャンネル登録日",
        "statistics.videoCount":"チャンネル動画数",        
        "statistics.viewCount":"チャンネル総再生回数",
        "statistics.subscriberCount":"チャンネル登録者数",
        "brandingSettings.channel.keywords":"SEO設定キーワード",
        "brandingSettings.channel.moderateComments":"コメント検閲設定",
        "brandingSettings.channel.featuredChannelsUrls":"おすすめチャンネル",
        "brandingSettings.channel.unsubscribedTrailer":"チャンネル未登録者おすすめ動画"
    }

    # extract
    db = PersitenceDatabaseConnector("youtube")
    try:
        db.connect()
        
        db.cursor.execute('select body from channels where create_date between %s and %s',[datetime.now().replace(hour=0,minute=0,second=0,microsecond=0),datetime.now().replace(hour=23,minute=59,second=59,microsecond=59)])
        data = [json.loads(d[0])["items"][0] for d in db.cursor.fetchall()]
    except db.errors.ProgrammingError as e:
        print(e)
        sys.exit()
    finally:
        db.close()

    # transform
    if len(data) ==0:
        raise Exception("データが取れてないよ")
    df = pd.json_normalize(data)
    filtered_column_neames =  {column_name:rename for column_name,rename in column_neames.items() if column_name in list(df.columns)}
    df = df[filtered_column_neames.keys()].rename(columns=filtered_column_neames)
    file_path = "channels" + datetime.now().strftime('%Y-%m-%d-%H%M%S')  + ".csv"
    df.to_csv(file_path)
    
    # load
    from boto3.session import Session
    cfg = configparser.SafeConfigParser(os.environ)
    cfg.read('./resource/settings/aws.cfg')
    arn=cfg["credential"]["arn"]

    client = boto3.client('sts')    
    response =  client.assume_role(
                RoleArn=arn,
                RoleSessionName="temp"
            )

    session = Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                    aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                    aws_session_token=response['Credentials']['SessionToken'],
                    region_name='ap-northeast-1')
    
    session.resource('s3').Bucket('youtube-channel-data').upload_file(file_path,"targetChannelsDumpCSV/" + file_path)

    # del transffered file.
    os.remove(file_path)

