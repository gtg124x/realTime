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

## The REST API format
curl -o ~/Desktop/file.json http://localhost:5000/realTimeEvent/api/v1.0/-33.5/-70.625