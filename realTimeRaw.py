#!/usr/bin/env python

#-----------------------------------------------------------------------
# flask is used for the REST API
#-----------------------------------------------------------------------
from flask import Flask, jsonify, request
app = Flask(__name__)


#-----------------------------------------------------------------------
# json is used to create a json object from geo-tagged tweets + cell info
#-----------------------------------------------------------------------
import json

#-----------------------------------------------------------------------
# used to for start and end time comparision
#-----------------------------------------------------------------------
from datetime import datetime

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
# creates a json of geo-tagged tweets + their cell info
# start is in the form YEAR-MN-DAY_HR:MIN with AM or PM
# for ex. 2019-06-10_5:18AM
#curl -i http://localhost:5000/todo/api/v1.0/tasks/<start>/<end>
#-----------------------------------------------------------------------
def get_tweets(start, end):

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

    # list to temp hold tweets; will be coverted to json at the end
    my_list =[]

    # had to have _ in it because url is used to pass start and end
    start = start.replace("_", " ")
    end = end.replace("_", " ")

    #create objects for comparision
    start_obj = datetime.strptime(start, '%Y-%m-%d %I:%M%p')
    end_obj = datetime.strptime(end, '%Y-%m-%d %I:%M%p')

    #DEBUG
    #print start_obj
    #print end_obj

    # Edge case of start time is past end time
    if start_obj > end_obj:
        return my_list

    # Busy wait until start time happens
    while start_obj > datetime.now():
        pass

    # Collect tweets
    for tweet in tweet_iter:

        # Make sure tweet has text or errors out because tweet has no json field
        if 'text' in tweet:

            # Only Retain geotagged tweets, which tweet-specific location information
            # falls into two general categories: tweets with a point or place
            # Tweets containing 'geo' or 'coordinates' metadata can also include
            # 'Twitter Place' data, although the presence of both is not guaranteed.
            # NOTE:'geo' has been depricated I think...
             # https://developer.twitter.com/en/docs/tutorials/filtering-tweets-by-location
            if tweet["place"] is not None or tweet["geo"] is not None or tweet["coordinates"] is not None:
                #DEBUG
                # print tweet["text"]
                # print tweet["geo"]
                # print tweet["coordinates"]
                # print tweet["place"]

                # Tweets with a Twitter 'Place' contain a polygon, consisting
                # of 4 lon-lat coordinates that define the general area the 'Place'
                # from which the user is posting the Tweet. Additionally, the Place
                # will have a display name, type (e.g. city, neighborhood), and
                # country code corresponding to the country where the Place is
                #located, among other fields.
                if tweet["place"] is not None:
                    long_lat = tweet["place"]["bounding_box"]["coordinates"]
                    # long_lat returns a polygon of 4 long_lat's
                    # We just need one to compute the cell
                    # Ex. [[[-92.227387, 13.72873], [-92.227387, 17.816205], [-88.221055, 17.816205], [-88.221055, 13.72873]]]
                    # The first dereference gets us into the list
                    # The second dereference gets us access to the first long_lat pair
                    # The third dereference gets access to long and latitude for manipulation in cell
                    longitude  = long_lat[0][0][0]
                    latitude = long_lat[0][0][1]

                # Tweets with a Point coordinate come from GPS enabled devices,
                # and represent the exact GPS location of the Tweet in question.
                # This type of location does not contain any contextual information
                # about the GPS location being referenced (e.g. associated city, country, etc.),
                # unless the exact location can be associated with a Twitter Place.
                # In the case of Twitter's enriched native format, the root
                # level "geo" and "coordinates" attributes provide the decimal
                # degree coordinates for the exact location.
                # Note: "coordinates" attributes is formatted as [LONGITUDE, latitude],
                # while "geo" attribute is formatted as [latitude, LONGITUDE].
                if tweet["coordinates"] is not None:
                    long_lat = tweet["coordinates"]["coordinates"]
                    longitude = long_lat[0]
                    latitude = long_lat[1]

                # NOTE: "geo" attribute is formatted as [latitude, LONGITUDE].
                if tweet["geo"] is not None:
                    lat_long = tweet["geo"]["coordinates"]
                    latitude = lat_long[0]
                    longitude = lat_long[1]

                # cell calculations
                row = int((90 + latitude) * 24)
                column = int((180 + longitude) * 24)
                row_column = str(row) + "_" + str(column)

                # add cell info to original tweet info
                tweet["row_column"] = row_column

                # Add tweet to list
                my_list.append(tweet)

                #DEBUG
                #print tweet
                #print('')

        # stop when current time is greater than end time
        if datetime.now() > end_obj:
            break

    #return list of tweets
    return my_list


@app.route('/todo/api/v1.0/tasks/<start>/<end>', methods=['GET'])
def get_tasks(start=None, end=None):

    # get list of geo-tagged tweets (original info + cell)
    my_list = get_tweets(start, end)

    # convert to json because flask demands it
    my_json_string = json.dumps(my_list)
    return my_json_string

# boiler plate
if __name__ == '__main__':
    app.run(debug=True)


