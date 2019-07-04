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
\i ~/realTime/realTimeEvent/sql/create_vw_events.sql
```

## This gets executed ever hour...
**EventRetriever (processes raw data into events, puts them into database) and marks if event belongs to cell**<br />
```
chmod a+x EventRetriever.py
./EventRetriever.py
```

## In a seperate termininal, Make the API executable and Run it
**This should also always be running to recieve requests from the Web app team and Android Team**<br />
```
chmod a+x EventAPI.py
./EventAPI.py
```

## The REST API Format
**The url is  http://localhost:5000/realTimeEvent/api/v1.0/<latitude>/<longitude>**<br />
Input: latitude, longitude<br />
Output: events (event_id (hashtag) + corresponding tweets) for a given cell<br />
An example is...<br />
```
http://localhost:5000/realTimeEvent/api/v1.0/50.4584/-3.583
```
You will receive back a json that is formatted like the following...<br />
```
{"endorphins": [
                "I just finished mountain biking 8.98 km in 38m:50s with #Endomondo #endorphins null",
                "I just finished running 8.67 km in 1h:00m:01s with #Endomondo #endorphins null",
                "I just finished cycling 12.75 km in 42m:31s with #Endomondo #endorphins null",
                "I just finished cycling 14.45 miles in 1h:08m:42s with #Endomondo #endorphins null"
                ],
  "Endomondo": [
                "I just finished cycling 12.75 km in 42m:31s with #Endomondo #endorphins null",
                "I just finished cycling 14.45 miles in 1h:08m:42s with #Endomondo #endorphins null",
                "I just finished mountain biking 8.98 km in 38m:50s with #Endomondo #endorphins null",
                "I just finished running 8.67 km in 1h:00m:01s with #Endomondo #endorphins null"
                ]
}
```

In this case the keys (event_ids) were "endorphins" and "Endomondo", and the values were an array of tweets for that event_id. <br />


