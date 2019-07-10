#!/usr/bin/env python

import psycopg2

import json

from configparser import ConfigParser


class EventDataBase( object ):

    @staticmethod
    def fn_update_is_event_cell():
        conn = EventDataBase.connect()
        # create a cursor
        cur = conn.cursor()
        cur.callproc('fn_update_is_event_cell')
        conn.commit()
        EventDataBase.end_connect(conn)


    @staticmethod
    def insert_tb_event( conn, hashtag, tweet, cell, created, id_str, latitude, longitude ):
        sql = """
                INSERT INTO tb_event(hashtag, tweet, cell, created, id_str, latitude, longitude )
                     VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_str) DO NOTHING;
              """
        # create a cursor
        cur = conn.cursor()
        cur.execute(sql, (hashtag, tweet, cell, created, id_str, latitude, longitude))
        conn.commit()

    @staticmethod
    def get_totaltweets( cell, dtmin, dtmax ):
        conn = EventDataBase.connect()
        sql = """
        SELECT COUNT(*)
          FROM tb_event
         WHERE cell = %s AND created BETWEEN %s AND %s
        """
        #print sql
        # create a cursor
        cur = conn.cursor()
        cur.execute(sql, (cell, dtmin, dtmax))
        row = cur.fetchone()
        count = row[0]
        cur.close()
        conn.close()
        return count 

    @staticmethod
    def get_totalevents( cell, dtmin, dtmax ):
        conn = EventDataBase.connect()
        sql = """
        SELECT COUNT(DISTINCT hashtag)
          FROM tb_event
         WHERE cell = %s AND created BETWEEN %s AND %s
        """
        #print sql
        # create a cursor
        cur = conn.cursor()
        cur.execute(sql, (cell, dtmin, dtmax))
        row = cur.fetchone()
        count = row[0]
        cur.close()
        conn.close()
        return count 

    def get_EventList_radius(latitude, longitude, radius):
        conn = EventDataBase.connect()
        radius = float(radius)
        latitude = float(latitude)
        longitude = float(longitude)

        #.1 decimal degree == 6.9 miles
        shift = (radius * 0.1) / 6.9

        latitude_top = latitude + shift
        latitude_bottom = latitude - shift
        longitude_left = longitude - shift
        longitude_right = longitude + shift

        sql = """
        SELECT hashtag,
               tweet,
               latitude,
               longitude
          FROM vw_event
         WHERE (latitude::double precision >= %s AND latitude::double precision <= %s)
           AND (longitude::double precision >= %s AND longitude::double precision <= %s);
        """

        cur = conn.cursor()
        cur.execute(sql, (latitude_bottom, latitude_top, longitude_left, longitude_right,))

        my_list = []

        for row in cur:
            temp_dict = {}
            hashtag = row[0]
            tweets = row[1]
            latitude = row[2]
            longitude = row[3]
            temp_dict["hashtag"] = hashtag
            temp_dict["tweets"] = tweets
            temp_dict["latitude"] = latitude
            temp_dict["longitude"] = longitude
            my_list.append(temp_dict)
        cur.close()
        conn.close()
        return my_list


    @staticmethod
    def get_EventList( cell ):
        conn = EventDataBase.connect()
        sql = """
        SELECT hashtag,
               tweet,
               latitude,
               longitude
          FROM vw_event
         WHERE cell = %s;
        """
        # create a cursor
        cur = conn.cursor()
        cur.execute(sql, (cell,))

        my_list = []

        for row in cur:
            temp_dict = {}
            hashtag = row[0]
            tweets = row[1]
            latitude = row[2]
            longitude = row[3]
            temp_dict["hashtag"] = hashtag
            temp_dict["tweets"] = tweets
            temp_dict["latitude"] = latitude
            temp_dict["longitude"] = longitude
            my_list.append(temp_dict)
        cur.close()
        conn.close()
        return my_list

    @staticmethod
    def get_topEvents( cell ):
        conn = EventDataBase.connect()
        sql = """
        SELECT hashtag,
               tweet
          FROM tb_event
         WHERE cell = %s;
        """
        # create a cursor
        cur = conn.cursor()
        cur.execute(sql, (cell,))
        events = {}

        for row in cur:
            hashtag = row[0]
            tweets = row[1]
            if hashtag not in events.keys():
                events[hashtag] = [tweets]
            else:
                events[hashtag].append(tweets)

        toptweets = max(len(i) for i in events.values())
        topevents = [key for key, i in events.items() if len(i) == toptweets and len(i) >= 2]
        
        cur.close()
        conn.close()
        return topevents 

    @staticmethod
    def end_connect(conn):

        # create a cursor
        cur = conn.cursor()
        # close the communication with the PostgreSQL
        cur.close()
        conn.close()


    @staticmethod
    def connect():
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = EventDataBase.config_db()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            #conn = psycopg2.connect(host="localhost",database="rawdatadb", user="gtg124x", password="")
            conn = psycopg2.connect(**params)

            # create a cursor
            cur = conn.cursor()

       # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

           # close the communication with the PostgreSQL
            #cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        # finally:
        #     if conn is not None:
        #         conn.close()
        #         print('Database connection closed.')

        return conn

    # The following config() function read the database.ini file and returns the connection parameters. We put the config() function in the config.py file:
    # http://www.postgresqltutorial.com/postgresql-python/connect/
    @staticmethod
    def config_db(filename='database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db
