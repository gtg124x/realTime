# RealTimeRaw
Twitter Streaming API
Objectives:
-learn virtualenv
-learn how to collect tweets using sample stream

virtualenv is a tool to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables to use the packages that a Python project would need.

##check if python is installed
python --version

#check if pip is installed
pip --version

#install virtualenv
pip install virtualenv

#check if virtualenv is installed correctly
virtualenv --version

#create project folder
mkdir realTime

#go to project folder
cd realTime

#create virtual environment for Python 2.7
virtualenv -p /usr/bin/python2.7 venv2.7

#activate newly created virtual environment
source venv2.7/bin/activate

#install Python Twitter Tools and flask
pip install twitter
virtualenv flask
pip install flask

#copy config.py from "twitter python sample code"
curl -O https://raw.githubusercontent.com/ideoforms/python-twitter-examples/master/config.py

#modify config.py accordingly
-consumer key, consumer secret key, access key, access key secret
    Consumer Key (API Key) = "WBv2tK1r07yKlqQohBnQXlFUe"
    Consumer Secret (API Secret) = "2o5bxMkhvlQnA1s6K3TkBPaS2EXSGf6jjwBVzvsKqT3VrTdWvq"
    Access Token API Key = "2478905953-wzRnECJQwmsUo6wuMdR78CHGw8OeXWIQcR2a5Fr"
    Access Token Secret = "YxzfAy2elUUnxA95pcGB4YZSmispN6xbGlXspoyvzoJim"

#copy realTimeRaw.py
curl -O https://raw.githubusercontent.com/ideoforms/python-twitter-examples/master/twitter-search.py

#make the application executable
chmod a+x realTime_app.py

#run the application
./realTime_app.py

#run to get output
# start and end is in the form YEAR-MN-DAY_HR:MIN with AM or PM concatenated
# Ex. 2019-06-10_5:18AM
curl -i http://localhost:5000/todo/api/v1.0/tasks/<start>/<end>

