#!/usr/bin/env python

#-----------------------------------------------------------------------
# flask is used for the REST API
#-----------------------------------------------------------------------
from flask import Flask, jsonify, request
app = Flask(__name__)

#-----------------------------------------------------------------------
# Function for getting events
#-----------------------------------------------------------------------
from EventDataBase import *


class EventAPI( object ):

    @app.route('/realTimeEvent/api/v2.1/<latitude>/<longitude>/<radius>', methods=['GET'])
    def get_tasks2(latitude=None, longitude=None, radius=None):

        # get list of geo-tagged tweets
        my_dict = EventDataBase.get_EventList_radius( latitude, longitude, radius )

        if my_dict is None:
            my_dict = 'no_events_for_cell'

        # convert to json because flask demands it
        my_json = json.dumps(my_dict)
        return my_json



    @app.route('/realTimeEvent/api/v2.1/<latitude>/<longitude>', methods=['GET'])
    def get_tasks(latitude=None, longitude=None):

        lat = 0
        longit = 0

        lat = float(latitude)
        longit = float(longitude)


        # cell calculations
        row = int((90 + lat) * 24)
        column = int((180 + longit) * 24)
        cell = str(row) + "_" + str(column)

        # get list of geo-tagged tweets (original info + cell)
        my_dict = EventDataBase.get_EventList( cell )

        if my_dict is None:
            my_dict = 'no_events_for_cell'

        # convert to json because flask demands it
        my_json = json.dumps(my_dict)
        return my_json


    @app.route('/realTimeEvent/api/v1.0/topevents/<latitude>/<longitude>', methods=['GET'])
    def get_topEvents(latitude=None, longitude=None):

        lat = 0
        longit = 0

        lat = float(latitude)
        longit = float(longitude)


        # cell calculations
        row = int((90 + lat) * 24)
        column = int((180 + longit) * 24)
        cell = str(row) + "_" + str(column)

        # get list of geo-tagged tweets (original info + cell)
        my_dict = EventDataBase.get_topEvents( cell )

        if my_dict is None:
            my_dict = 'no_events_for_cell'

            #my_json_string = dict(my_list)

        # convert to json because flask demands it
        my_json = json.dumps(my_dict)
        return my_json

    @app.route('/realTimeEvent/api/v1.0/totaltweets/<latitude>/<longitude>/<dt>', methods=['GET'])
    def get_totaltweets(latitude=None, longitude=None, dt=None):

        lat = 0
        longit = 0

        lat = float(latitude)
        longit = float(longitude)


        # cell calculations
        row = int((90 + lat) * 24)
        column = int((180 + longit) * 24)
        cell = str(row) + "_" + str(column)

        dtmin = dt + " 00:00:00"
        dtmax = dt + " 23:59:59"

        # get list of geo-tagged tweets (original info + cell)
        count = EventDataBase.get_totaltweets( cell, dtmin, dtmax )

        if count < 1:
            count = 'no_events_for_cell'

            #my_json_string = dict(my_list)

        # convert to json because flask demands it
        my_json = json.dumps(count)
        return my_json

    @app.route('/realTimeEvent/api/v1.0/totalevents/<latitude>/<longitude>/<dt>', methods=['GET'])
    def get_totalevents(latitude=None, longitude=None, dt=None):

        lat = 0
        longit = 0

        lat = float(latitude)
        longit = float(longitude)


        # cell calculations
        row = int((90 + lat) * 24)
        column = int((180 + longit) * 24)
        cell = str(row) + "_" + str(column)

        dtmin = dt + " 00:00:00"
        dtmax = dt + " 23:59:59"

        # get list of geo-tagged tweets (original info + cell)
        count = EventDataBase.get_totalevents( cell, dtmin, dtmax )

        if count < 1:
            count = 'no_events_for_cell'

            #my_json_string = dict(my_list)

        # convert to json because flask demands it
        my_json = json.dumps(count)
        return my_json

    # boiler plate
    if __name__ == '__main__':
        app.run(debug=True, port=6000)
