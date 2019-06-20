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

## Copy config.py from "twitter python sample code"
curl -O https://raw.githubusercontent.com/ideoforms/python-twitter-examples/master/config.py

## Modify config.py accordingly
Consumer Key (API Key) = "WBv2tK1r07yKlqQohBnQXlFUe"<br />
Consumer Secret (API Secret) = "2o5bxMkhvlQnA1s6K3TkBPaS2EXSGf6jjwBVzvsKqT3VrTdWvq"<br />
Access Token API Key = "2478905953-wzRnECJQwmsUo6wuMdR78CHGw8OeXWIQcR2a5Fr"<br />
Access Token Secret = "YxzfAy2elUUnxA95pcGB4YZSmispN6xbGlXspoyvzoJim"<br />

## Download realTimeRaw.py
git clone https://github.com/gtg124x/realTimeRaw.git

## Make the application executable
chmod a+x realTimeRaw.py

## Run the application
./realTimeRaw.py

## API 
http://localhost:5000/realTimeRaw/api/v1.0/<start><end><br />
<br />
Start and end is in the form YEAR-MN-DAY_HR:MIN with AM or PM concatenated<br />
Ex. 2019-06-10_5:18AM<br />  

## Run to get output
curl -o target/path/filename URL<br />
--EX. curl -o ~/Desktop/file.json http://localhost:5000/realTimeRaw/api/v1.0/2019-06-16_12:01AM/2019-06-20_12:05AM<br />

