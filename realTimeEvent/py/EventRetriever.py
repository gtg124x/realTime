#!/usr/bin/env python

import requests
import json
from EventDataBase import *
import datetime

class EventRetriever( object ):

    @staticmethod
    def tryit():
        get_url = EventRetriever().set_up_API_call()
        EventRetriever().insertEvents( get_url )
        EventDataBase.fn_update_is_event_cell()

    @staticmethod
    def set_up_API_call():

        # This controls the time interval to pull tweets from the Raw Data Server
        REALTIME  = 60
        now       = datetime.datetime.now()
        start     = now - datetime.timedelta(minutes=REALTIME)
        start_url = str(start)
        start_url = start_url.replace(" ", "_")
        end_url   = now.strftime("%Y-%m-%d_%H:%M")

        # The agreed upon API
        get_url = "http://localhost:6000/realTimeRaw/api/v2.0/" + start_url + "/" + end_url

        print get_url

        return get_url

    @staticmethod
    def insertEvents( get_url ):

        #get_r = requests.get(url=get_url)

        #data = get_r.json()

        # Open Connection with Database

        conn = EventDataBase.connect()

        with requests.get(get_url, stream=True) as r:
            r.raise_for_status()
            with open('new.json', 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)


        with open('new.json') as json_file:
            data = json.load(json_file)
            for tweet in data:
                if len(tweet[0]["entities"]["hashtags"]) != 0:
                    id_str = tweet[0]["id_str"]
                    text = tweet[0]["text"]
                    cell = tweet[0]["cell"]
                    created = tweet[0]["created"]
                    latitude = tweet[0]["raw_latitude"]
                    longitude = tweet[0]["raw_longitude"]

                    for hashgroup in tweet[0]["entities"]["hashtags"]:

                        for hashtag_candidate in hashgroup:

                            if hashtag_candidate == "text":
                                hashtag = hashgroup["text"]
                                EventDataBase.insert_tb_event(conn, hashtag, text, cell, created, id_str, latitude, longitude )

        # End Database Connection
        EventDataBase.end_connect(conn)

if __name__ == '__main__':
    get_url = EventRetriever().set_up_API_call()
    EventRetriever().insertEvents( get_url )
    EventDataBase.fn_update_is_event_cell()

