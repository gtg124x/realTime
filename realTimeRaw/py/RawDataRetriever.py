#!/usr/bin/env python

#-----------------------------------------------------------------------
# json is used to create a json object from geo-tagged tweets + cell info
#-----------------------------------------------------------------------
import json

#-----------------------------------------------------------------------
# twitter-stream-format:
#  - ultra-real-time stream of twitter's public timeline.
#    does some fancy output formatting.
#-----------------------------------------------------------------------
from twitter import *
import re

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
import sys
sys.path.append(".")
import config

#-----------------------------------------------------------------------
# Filter class has methods to retain geo-tagged tweets
#-----------------------------------------------------------------------
from RawDataFilter import *

#-----------------------------------------------------------------------
# Adds cell data to original tweet data
#-----------------------------------------------------------------------
from RawDataCellProcessor import *

#-----------------------------------------------------------------------
# Inserts tweet into database
#-----------------------------------------------------------------------
from RawDataBase import *

#-----------------------------------------------------------------------
# creates a json of geo-tagged tweets + their cell info
# start is in the form YEAR-MN-DAY_HR:MIN with AM or PM
# for ex. 2019-06-10_5:18AM
#curl -i http://localhost:5000/todo/api/v1.0/tasks/<start>/<end>
#-----------------------------------------------------------------------
class RawDataRetriever( object ):
    #-----------------------------------------------------------------------
    # create twitter streaming API object
    #-----------------------------------------------------------------------
    auth = OAuth(config.access_key,
                 config.access_secret,
                 config.consumer_key,
                 config.consumer_secret)
    stream = TwitterStream(auth = auth, secure = True)

    #-----------------------------------------------------------------------
    # iterate over tweets matching this filter text
    #-----------------------------------------------------------------------
    tweet_iter = stream.statuses.sample()

    # inside the permiter
    # tweet_iter = stream.statuses.filter(locations = "-84.5,33.6,-84.25,33.92")

    # Just ATL cell 2970_2294
    #tweet_iter = stream.statuses.filter(locations = "-84.41,33.75,-84.38,33.79")

    # USA
    tweet_iter = stream.statuses.filter(locations = "-124.7771694, 24.520833, -66.947028, 49.384472")

    # Open Connection with Database
    conn = RawDataBase.connect()

     # Collect tweets
    for tweet in tweet_iter:

        # Check if tweet is actually a tweet
        if 'text' in tweet:

            # Retain only geo-tagged tweets
            if RawDataFilter.isGeoTagged(tweet):

                # Add cell info to original tweet info
                tweet = RawDataCellProcessor.addCellData(tweet);

                # Add tweet to database
                RawDataBase.insert_tb_rawData(conn, tweet)

                # DEBUG
                print tweet

    # End Database Connection
    RawDataBase.end_connect(conn)

