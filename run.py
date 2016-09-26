#!flask/bin/python3
from app import app
app.run(processes=2, debug=True)#REMOVE DEBUG IN PRODUCTION
