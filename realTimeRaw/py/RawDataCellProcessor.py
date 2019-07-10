#!/usr/bin/env python

import datetime

class RawDataCellProcessor( object ):

    @staticmethod
    def addCellData( tweet ):

        # Tweets with a Twitter 'Place' contain a polygon, consisting
        # of 4 lon-lat coordinates that define the general area the 'Place'
        # from which the user is posting the Tweet. Additionally, the Place
        # will have a display name, type (e.g. city, neighborhood), and
        # country code corresponding to the country where the Place is
        #located, among other fields.
        if tweet["place"] is not None:
            if tweet["place"]["bounding_box"] is not None:
                if tweet["place"]["bounding_box"]["coordinates"] is not None:
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
        tweet["cell"]      = row_column

        now                = datetime.datetime.now()
        now_str            = str(now)
        tweet["created"] = now_str
        tweet["raw_latitude"] = latitude
        tweet["raw_longitude"] = longitude

        return tweet



