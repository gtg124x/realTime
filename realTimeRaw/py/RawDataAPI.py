#!/usr/bin/env python

#-----------------------------------------------------------------------
# flask is used for the REST API
#-----------------------------------------------------------------------
from flask import Flask, jsonify, request
app = Flask(__name__)

#-----------------------------------------------------------------------
# Function for getting tweets
#-----------------------------------------------------------------------
from RawDataBase import *

class RawDataAPI( object ):

    @app.route('/realTimeRaw/api/v2.0/<start>/<end>', methods=['GET'])
    def get_tasks(start=None, end=None):



        # had to have _ in it because url is used to pass start and end
        start = start.replace("_", " ")
        end = end.replace("_", " ")

        conn = RawDataBase.connect()

        # get list of geo-tagged tweets (original info + cell)
        my_list = RawDataBase.get_rawData( conn, start, end )

        # End Database Connection
        RawDataBase.end_connect(conn)

        # convert to json because flask demands it
        my_json_string = json.dumps(my_list)
        return my_json_string


    # boiler plate
    if __name__ == '__main__':
        app.run(debug=True)