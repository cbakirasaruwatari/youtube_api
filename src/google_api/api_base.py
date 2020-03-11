#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# google apis
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# base
import os
import sys
import json
import configparser
from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass

from db import PersitenceDatabaseConnector as Pdbc

class EndpointAccessor:

   _CFG_PATH:str = './resource/settings/api.cfg'

   def __init__(
                self,
                api_service_name: str=None
                # cfg_path: str=None
               ) -> None:
      if api_service_name == None:
         pass
      else:
         self.set(api_service_name)

   def set(self,api_service_name: str):
      if os.path.isfile(self._CFG_PATH) is False:
         raise FileNotFoundError    
      cfg = configparser.SafeConfigParser(os.environ)
      cfg.read(self._CFG_PATH)

      self.api_service_name = cfg[api_service_name]["API_SERVICE_NAME"]
      self.api_version = cfg[api_service_name]["API_VERSION"]

      self.acs = self.__build(self.api_service_name,
                              self.api_version,
                              cfg["auth"]["API_DEVELOPPER_KEY"]
                              )

   def __build(self,service_name: str, version: str,key:str):
      return build(service_name, version,developerKey=key)
   
   def get(self,method:str,**options):
      return getattr(self.acs,method)().list(**options).execute()

class APIMeta(metaclass = ABCMeta):
   @dataclass(frozen=True) 
   class Destination:
      db:str="mysql"
      file:str="json"

   def __init__(self,service_name: str,destination: str,resource: str = "file"):
      self.accssr = EndpointAccessor(service_name)

      for ent,arg in zip(["Destination"],[destination]):
         if hasattr(getattr(self,ent),arg) == False:
            raise AttributeError(ent + " is Wrong")
      if destination == "db" or resource == "db":
         self.db = Pdbc(service_name)
      
   @abstractmethod
   def start(self):
      raise NotImplementedError





