#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# base
import os
import sys
import json
# import csv

from api_base import APIMeta

class APIYoutube(APIMeta):

   def __init__(self,method,*,destination,resource):
      if destination is None:
         raise ValueError(" must input destionation arg")
      elif resource is None:
         raise ValueError(" must input resource arg")
      super(APIYoutube, self).__init__("youtube", destination,resource)
      self.method = method
      self.destination = destination
      self.resource = resource

   def start(self) -> None:
      targets = self.__fetch_target(self.method,self.resource)
      for target in targets:
         result = self.__run(id = target,part="id,snippet,brandingSettings,contentDetails,invideoPromotion,statistics,topicDetails")
         self.__save(self.destination,self.method,json.dumps(result))

   def __run(self,**options) -> None:
      result:dict = self.accssr.get(method=self.method,**options)

      return result
   
   def __fetch_target(self,method_name: str,resource: str=None) -> list:
      if resource == "file":
         return self.__fetch_target_from_file(method_name)
      elif resource == "db":
         return self.__fetch_target_from_db(method_name + "_resource")
      else: 
         raise NotImplementedError

   def __fetch_target_from_file(self,dir_name:str) -> list:
      targets = []
      target_dir = "./resource/youtube/" + dir_name + "/"
      target_files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
      if len(target_files) > 1:
         raise NotImplementedError("not support mutiple files")
      elif len(target_files) <= 0:
         raise FileNotFoundError("must has a target file")
      for file in target_files:
         with open(target_dir + file) as r:
            targets.extend([url[url.rfind("/")+1:] for url in json.load(r)])
      
      return targets

   def __fetch_target_from_db(self,tbl_name:str) -> list:
      self.db.connect()
      self.db.cursor.execute('select url from ' +  tbl_name + " order by create_date asc")
      targets = [ url[0][url[0].rfind("/")+1:] for url in self.db.cursor.fetchall()]

      return targets

   def __save(self,destination: str,name: str,body: json) -> None:
      if destination == "db":
         self.__save_to_mysql(name,body)
      else: 
         raise NotImplementedError

   def __save_to_mysql(self,tbl_name: str, body: json) -> None:
      try:
         body_li = json.loads(body)
         self.db.connect()
         self.db.cursor.execute("INSERT INTO " + tbl_name +  " (original_id,api_method,api_version,body) VALUES (%s,%s,%s,%s)",[body_li["etag"],body_li["kind"],self.accssr.api_version,body])
         self.db.commit()
      except self.db.errors.ProgrammingError as e:
         print(e)
         sys.exit()
      finally:
         self.db.close()

if __name__ == "__main__":
   print("start getting channels")
   channel = APIYoutube("channels",destination="db",resource="db")
   channel.start()
   print("finish getting channels")




   # channel = APIYoutube("channels",destination="db",resource="db")
   # target_dir = "./resource/youtube/" + "channels" + "/"
   # target_files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
   # targets = []
   # with open(target_dir + target_files[0]) as r:
   #       targets.extend([url[url.rfind("/")+1:] for url in json.load(r)])
   # for temp in  targets:
   #    channel.db.connect()
   #    channel.db.cursor.execute("INSERT INTO youtube.channels_resource (url, create_date) VALUES(%s, CURRENT_TIMESTAMP)",[temp])
   #    channel.db.commit()




   
