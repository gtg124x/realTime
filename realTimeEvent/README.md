# RealTimeEvent

## Install Python Tools
```
pip install requests
```

## In a seperate termininal, Create Database and Table
```
psql postgres
\i ~/realTime/realTimeEvent/sql/create_eventdb.sql
\q
psql eventdb
\i ~/realTime/realTimeEvent/sql/create_tb_event.sql
\i ~/realTime/realTimeEvent/sql/fn_update_is_event_cell.sql
\i ~/realTime/realTimeEvent/sql/create_vw_event.sql
```

## In a seperate terminal, Run the jobScheduler.py
**This runs the EventRetriever (processes raw data into events, puts them into database) and marks if event belongs to cell each hour (real time is 1 hour)**<br />
**jobScheduler runs this script every hour**<br />
```
chmod a+x EventRetriever.py
chmod a+x jobScheduler.py
./jobScheduler.py
```

## In a seperate termininal, Make the API executable and Run it
**This should also always be running to recieve requests from the Web app team and Android Team**<br />
```
chmod a+x EventAPI.py
./EventAPI.py
```

## The REST API Format
**The url for a cell is  http://localhost:6000/realTimeEvent/api/v2.0/latitude/longitude**<br />
Input: latitude, longitude<br />
Output: events (event_id (hashtag) + corresponding tweets + latitude + longitude) for a given cell<br />
<br />
**The url to get a cell and its radius  http://localhost:6000/realTimeEvent/api/v2.0/latitude/longitude/radius**<br />
Input: latitude, longitude, radius(in miles)<br />
Output: events (event_id (hashtag) + corresponding tweets + latitude + longitude) for a given radius surrounding a cell<br />

An example of just getting events for a cell in atlanta is...<br />
```
http://localhost:6000/realTimeEvent/api/v2.1/33.755/-84.39
```

An example of just getting events for a region with a 20 miles radius surrounding a cell in atlanta is...<br />
```
http://localhost:6000/realTimeEvent/api/v2.1/33.755/-84.39/20
```

You will receive back a json that is formatted like the following...<br />
```
[ { "hashtag" :
    "tweets" :
    "latitude" :
    "longitude" : },
  { "hashtag" :
    "tweets" :
    "latitude" :
    "longitude" : },
        .
        .
        .
]
```
An Example is...<br />
```
[{"tweets": ["It\u2019s our honor to swear in @KsandvikBESD33 as AASA 2019-20 President-Elect! Congratulations, Kristi! #AASAadv https://t.co/Jh8ikggUu2", "Look at all of our new Executive Committee Members! Congratulations and thank you for your service #AASAadv https://t.co/da9rW7Ohna"], "latitude": "38.801826", "longitude": "-77.119401", "hashtag": "AASAadv"}, {"tweets": ["We're hiring! Read about our latest job opening here: Network Engineer, Mid - https://t.co/tf6QYbPV8e #BoozAllen #IT", "Interested in a job in Annapolis Junction, MD? This could be a great fit: https://t.co/nQ1Sox8Oys #BoozAllen #Finance"], "latitude": "39.1202934", "longitude": "-76.7769324", "hashtag": "BoozAllen"}]
```

<br />
For debugging, the following redirects the output to a file on the desktop<br />
curl -o ~/Desktop/file.json http://localhost:6000/realTimeEvent/api/v2.1/33.755/-84.39<br />





