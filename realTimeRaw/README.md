# RealTimeRaw

## Check if python is installed
```
python --version
```

## Check if pip is installed
```
pip --version
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

## Install virtualenv
```
pip install virtualenv
```

## Check if virtualenv is installed correctly
```
virtualenv --version
```

## Create project folder
```
mkdir realTime
```

## Go to project folder
```
cd realTime
```

## Create virtual environment for Python 2.7
```
virtualenv -p /usr/bin/python2.7 venv2.7
```

## Activate newly created virtual environment
```
source venv2.7/bin/activate
```

## Install Python Twitter Tools and Flask
```
pip install twitter
virtualenv flask
pip install flask
pip install postgresql
pip install psycopg2-binary
pip install configparser
```

## Copy config.py from "twitter python sample code"
```
curl -O https://raw.githubusercontent.com/ideoforms/python-twitter-examples/master/config.py
```

## Modify config.py accordingly
```
Consumer Key (API Key) = "WBv2tK1r07yKlqQohBnQXlFUe"
Consumer Secret (API Secret) = "2o5bxMkhvlQnA1s6K3TkBPaS2EXSGf6jjwBVzvsKqT3VrTdWvq"
Access Token API Key = "2478905953-wzRnECJQwmsUo6wuMdR78CHGw8OeXWIQcR2a5Fr"
Access Token Secret = "YxzfAy2elUUnxA95pcGB4YZSmispN6xbGlXspoyvzoJim"
```

## Download realTimeRaw.py
```
git clone https://github.com/gtg124x/realTimeRaw.git
```

## In a seperate termininal, Create Database and table
```
psql postgres
\i ~/realTime/realTimeRaw/sql/create_rawdatadb.sql
\q
psql rawdatadb
\i ~/realTime/realTimeRaw/sql/create_tb_rawdata.sql
\q
```

## In a seperate termininal, Make the application executable and Run it
**This script would be running 24/7 streaming tweets from Twitter and inserting them into the database (with cell info)**<br />
```
chmod a+x RawDataRetriever.py
./RawDataRetriever.py
```

## In a seperate termininal, Make the API executable and Run it
**This should also always be running to recieve requests from the Event Server**<br />
```
chmod a+x RawDataAPI.py
./RawDataAPI.py
```

## The REST API format
**Format is http://localhost:5000/realTimeRaw/api/v2.0/start/end**<br />
<br />
Start and end is in the form YEAR-MN-DAY_HR:MIN:SEC<br />
```
Ex. 2019-06-10_5:18:00
```
<br />
For debugging, the following redirects the output to a file on the desktop<br />
```
curl -o target/path/filename URL
--EX. curl -o ~/Desktop/file.json http://localhost:5000/realTimeRaw/api/v2.0/2019-07-02_04:47:00/2019-07-02_04:50:00
```