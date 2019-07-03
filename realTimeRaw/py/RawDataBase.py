#!/usr/bin/env python

import psycopg2

import json

from configparser import ConfigParser


class RawDataBase( object ):

    @staticmethod
    def insert_tb_rawData( conn, tweet):
        created = tweet["created"]
        sql = """INSERT INTO tb_rawdata (tweet, created) VALUES(%s, %s);"""
        # create a cursor
        cur = conn.cursor()
        cur.execute(sql, (json.dumps(tweet),created,))
        conn.commit()

    @staticmethod
    def get_rawData( conn, start, end ):
        sql = """SELECT tweet FROM tb_rawdata
                  WHERE created >= %s::timestamp
                    AND created <= %s::timestamp;"""
        # create a cursor
        cur = conn.cursor()
        cur.execute(sql, (start, end,))
        results = cur.fetchall()
        return results

    @staticmethod
    def end_connect(conn):

        # create a cursor
        cur = conn.cursor()
        # close the communication with the PostgreSQL
        cur.close()


    @staticmethod
    def connect():
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = RawDataBase.config_db()

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