Relies on Python packages `flask` , `flask-restful`, `flask-wtf`, `pygit2`. These can be install with pip.


to set up virtual environment, assuming python 3:
* pyvenv flask
* flask/bin/pip3 install flask-restful
* flask/bin/pip3 install flask-wtf
* flask/bin/pip3 installrequests
* flask/bin/pip3 install pygit2

To run: `python run.py` or `python3 run.py` will start the server.

Then curl:

`curl -i -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1.0/anonymize -d '{"url": "https://github.com/github/testrepo.git", "description": "hello"}'`

NOTE: you will need an additional credentials file to run this. Please contact the creator directly if interested.
