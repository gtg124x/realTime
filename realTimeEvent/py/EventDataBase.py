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
    def insert_tb_event( conn, hashtag, tweet, cell, created, id_str ):
        sql = """
                INSERT INTO tb_event(hashtag, tweet, cell, created, id_str )
                     VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id_str) DO NOTHING;
              """
        # create a cursor
        cur = conn.cursor()
        cur.execute(sql, (hashtag, tweet, cell, created, id_str,))
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
    def get_EventList( cell ):
        conn = EventDataBase.connect()
        sql = """
        SELECT hashtag,
               tweet
          FROM tb_event
         WHERE cell = %s;
        """
        #print sql
        # create a cursor
        cur = conn.cursor()
        cur.execute(sql, (cell,))
        my_dict = {}
        for key, value in cur:
            if key is not None and value is not None:
                # key = event[0]
                # [value] = event[1]
                my_dict[key] = value
                #print value
        cur.close()
        conn.close()
        return my_dict

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
