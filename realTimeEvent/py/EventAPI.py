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
from EventGetter import *


class EventAPI( object ):

    @app.route('/realTimeEvent/api/v1.0/<latitude>/<longitude>', methods=['GET'])
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
        my_list = EventGetter.getEventList( cell )

        # convert to json because flask demands it
        my_json_string = json.loads(my_list)
        return my_json_string


    # boiler plate
    if __name__ == '__main__':
        app.run(debug=True)