# RealTimeRaw
Twitter Streaming API<br />
Objectives:<br />
-learn virtualenv<br />
-learn how to collect tweets using sample stream<br />

virtualenv is a tool to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables to use the packages that a Python project would need.<br />

## Check if python is installed
python --version<br />

## Check if pip is installed
pip --version<br />
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py<br />
python get-pip.py<br />

## Install virtualenv
pip install virtualenv

## Check if virtualenv is installed correctly
virtualenv --version

## Create project folder
mkdir realTime

## Go to project folder
cd realTime

## Create virtual environment for Python 2.7
virtualenv -p /usr/bin/python2.7 venv2.7

## Activate newly created virtual environment
source venv2.7/bin/activate

## Install Python Twitter Tools and flask
pip install twitter<br />
virtualenv flask<br />
pip install flask<br />
pip install postgresql<br />
pip install psycopg2-binary<br />
pip install configparser<br />

## Copy config.py from "twitter python sample code"
curl -O https://raw.githubusercontent.com/ideoforms/python-twitter-examples/master/config.py

## Modify config.py accordingly
Consumer Key (API Key) = "WBv2tK1r07yKlqQohBnQXlFUe"<br />
Consumer Secret (API Secret) = "2o5bxMkhvlQnA1s6K3TkBPaS2EXSGf6jjwBVzvsKqT3VrTdWvq"<br />
Access Token API Key = "2478905953-wzRnECJQwmsUo6wuMdR78CHGw8OeXWIQcR2a5Fr"<br />
Access Token Secret = "YxzfAy2elUUnxA95pcGB4YZSmispN6xbGlXspoyvzoJim"<br />

## Download realTimeRaw.py
git clone https://github.com/gtg124x/realTimeRaw.git

## In a seperate termininal, Create Database and table
psql postgres<br />
\i ~/realTime/realTimeRaw/sql/create_rawdatadb.sql<br />
\q<br />
psql rawdatadb<br />
\i ~/realTime/realTimeRaw/sql/create_tb_rawdata.sql<br />
\q<br />

## In a seperate termininal, Make the application executable and Run it
This script would be running 24/7 streaming tweets from Twitter and inserting them into the database (with cell info)<br />
chmod a+x RawDataRetriever.py<br />
./RawDataRetriever.py<br />

## In a seperate termininal, Make the API executable and Run it
This should also always be running to recieve requests from the Event Server<br />
chmod a+x RawDataAPI.py<br />
./RawDataAPI.py<br />

## The REST API format
Format is http://localhost:5000/realTimeRaw/api/v2.0/start/end<br />
<br />
Start and end is in the form YEAR-MN-DAY_HR:MIN:SEC<br />
Ex. 2019-06-10_5:18:00<br />
<br />
For debugging, the following redirects the output to a file on the desktop<br />
curl -o target/path/filename URL<br />
--EX. curl -o ~/Desktop/file.json http://localhost:5000/realTimeRaw/api/v2.0/2019-07-02_04:47:00/2019-07-02_04:50:00<br />