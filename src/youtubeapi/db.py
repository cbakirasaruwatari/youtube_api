#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# base
import os
import sys
import configparser
import mysql.connector as mydb

class PersitenceDatabaseConnector:
  _CFG_PATH:str = './resource/settings/db.cfg'
  errors = mydb.errors
  def __init__(
                self,
                db_name: str
              ):

    if os.path.isfile(self._CFG_PATH) is False:
        raise FileNotFoundError
    cfg = configparser.SafeConfigParser(os.environ)
    cfg.read(self._CFG_PATH)

    self.__host=cfg["persistance_db"]["db_host"]
    self.__port=cfg["persistance_db"]["db_port"]
    self.__user=cfg["persistance_db_" + db_name]["db_user"]
    self.__password=cfg["persistance_db_" + db_name]["db_password"]
    self.__database=cfg["persistance_db_" + db_name]["db_database"]

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
