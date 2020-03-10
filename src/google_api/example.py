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
import re 
import traceback
import configparser
import csv
import datetime

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEVELOPER_KEY = "AIzaSyDdkIrh46hAcqAF8vOrG16Ol-4O3GMcFEI"

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.


def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.

  search_response = youtube.channels().list(
    # q=options.q,
    id=options["c"],
    # part="id,snippet,brandingSettings,contentDetails,invideoPromotion,statistics,topicDetails",
    part="snippet,statistics",
    maxResults=options["max_results"]
  ).execute()

  videos = []
  channels = []
  playlists = []

  return search_response.get("items", [])

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  # for search_result in search_response.get("items", []):
  #   if search_result["id"]["kind"] == "youtube#video":
  #     videos.append("%s (%s)" % (search_result["snippet"]["title"],
  #                                search_result["id"]["videoId"]))
  #   elif search_result["id"]["kind"] == "youtube#channel":
  #     channels.append("%s (%s)" % (search_result["snippet"]["title"],
  #                                  search_result["id"]["channelId"]))
  #   elif search_result["id"]["kind"] == "youtube#playlist":
  #     playlists.append("%s (%s)" % (search_result["snippet"]["title"],
  #                                   search_result["id"]["playlistId"]))

  # print("Videos:\n", "\n".join(videos), "\n")
  # print("Channels:\n", "\n".join(channels), "\n")
  # print(search_response.get("items", []))  

if __name__ == "__main__":
  # argparser.add_argument("--q", help="Search term", default="Google")
  # argparser.add_argument("-c", help="channelid", default="Google",required=True)
  # argparser.add_argument("--max-results", help="Max results", default=25)
  # args = argparser.parse_args()

  # try:
  #   youtube_search(args)
  # except HttpError as e:
  #     print(e)

  with open('resource/target/url_list.json') as f:
      li = json.load(f)
    
  result = []
  for url in li:
    try:
      channel_id = url[url.rfind("/")+1:]
      re = youtube_search({"c":channel_id,"max_results":25})
      result.append({
        "title":re[0]["snippet"]["localized"]["title"],
        "description":re[0]["snippet"]["localized"]["description"],
        "url":url,
        "subscriberCount":re[0]["statistics"]["subscriberCount"],
        "videoCount":re[0]["statistics"]["videoCount"]
      })
    except HttpError as e:
      print(e)
      continue
    except IndexError:
      traceback.print_exc()
      print(re)
      continue
    except Exception as e:
      traceback.print_exc()
      print("eeee")
      sys.exit()



  header = result[0].keys()
  
  with open("./result/" + str(datetime.datetime.now()) + ".csv", 'w') as f:
    fieldnames = header
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in result:
        writer.writerow(row)
