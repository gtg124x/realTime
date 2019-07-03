pip install requests

## Install Python Tools

## In a seperate termininal, Create Database and Table
psql postgres<br />
\i ~/realTime/realTimeEvent/sql/create_eventdb.sql<br />
\q<br />
psql eventdb<br />
\i ~/realTime/realTimeEvent/sql/create_tb_event.sql<br />

----

Create view1 of this 24 hours (now, now - 24)
Create view 2of "past" 24 hours, shifted off 1 hour (now - 1hr, now - 2hr)
views will have hashtag, array of tweets, count of tweets, cell, created

Create view3 of hashtag and preform chi equation of two count columns
view will have hashtag and chi value

select from view 1 but only the hashtags that have a positive chi from view3 and is marked owned



SELECT * FROM tb_rawdata
                  WHERE created >= '2019-07-03 05:47:46.715599'::timestamp
                    AND created <= '2019-07-03 06:47'::timestamp order by created ASC limit 1;


WITH event_list AS (select hashtag,
                    array_agg(tweet) as tweet,
                    COUNT (tweet) as count
                    FROM tb_event
                    WHERE cell = '3153_2504'
                      AND created >= '2019-07-02 08:43:31.729735'::timestamp
                      AND created < '2019-07-02 10:45:31.729735'::timestamp
                 GROUP BY hashtag
                 ORDER BY count desc
                    LIMIT 500)
, event_historical AS (
                    select hashtag,
                    array_agg(tweet) as tweet,
                    COUNT (tweet) as count
                    FROM tb_event
                    WHERE cell = '3153_2504'
                      AND created >= '08:43:31.729735'::time
                      AND created < '10:45:31.729735'::time
                 GROUP BY hashtag
                 ORDER BY count desc
                    LIMIT 500
)
    select * from event_list;




## run these two each hour...
** EventRetriever (processes raw data into events, puts them into database) **<br />
** Function that determines what is the first cell to contain a hashtag and marks that as the event cell **<br />
chmod a+x EventRetriever.py<br />
./EventRetriever.py<br />
\i ~/realTime/realTimeEvent/sql/fn_update_is_event_cell.sql<br />

## In a seperate termininal, Make the API executable and Run it
This should also always be running to recieve requests from the Web app team and Android Team<br />
chmod a+x EventAPI.py<br />
./EventAPI.py<br />


## The REST API format



