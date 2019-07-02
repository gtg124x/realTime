#!/usr/bin/env python
class RawDataFilter( object) :

    @staticmethod
    def isGeoTagged( tweet ):

        # Only Retain geotagged tweets, which tweet-specific location information
        # falls into two general categories: tweets with a point or place
        # Tweets containing 'geo' or 'coordinates' metadata can also include
        # 'Twitter Place' data, although the presence of both is not guaranteed.
        # NOTE:'geo' has been depricated I think...
        # https://developer.twitter.com/en/docs/tutorials/filtering-tweets-by-location
        if tweet["place"] is not None or tweet["geo"] is not None or tweet["coordinates"] is not None:
            return True

        return False