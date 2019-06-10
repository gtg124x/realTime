# RealTimeRaw
Twitter Streaming API
Objectives:
-learn virtualenv
-learn how to collect tweets using sample stream

virtualenv is a tool to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables to use the packages that a Python project would need.

## Check if python is installed
python --version

## Check if pip is installed
pip --version
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

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
pip install twitter
virtualenv flask
pip install flask

## Copy config.py from "twitter python sample code"
curl -O https://raw.githubusercontent.com/ideoforms/python-twitter-examples/master/config.py

## Modify config.py accordingly
-consumer key, consumer secret key, access key, access key secret
    Consumer Key (API Key) = "WBv2tK1r07yKlqQohBnQXlFUe"
    Consumer Secret (API Secret) = "2o5bxMkhvlQnA1s6K3TkBPaS2EXSGf6jjwBVzvsKqT3VrTdWvq"
    Access Token API Key = "2478905953-wzRnECJQwmsUo6wuMdR78CHGw8OeXWIQcR2a5Fr"
    Access Token Secret = "YxzfAy2elUUnxA95pcGB4YZSmispN6xbGlXspoyvzoJim"

## Copy realTimeRaw.py
curl -O https://raw.githubusercontent.com/ideoforms/python-twitter-examples/master/twitter-search.py

## Make the application executable
chmod a+x realTimeRaw.py

## Run the application
./realTimeRaw.py

## Run to get output
curl -i http://localhost:5000/todo/api/v1.0/tasks/<start>/<end>
Start and end is in the form YEAR-MN-DAY_HR:MIN with AM or PM concatenated
Ex. 2019-06-10_5:18AM


