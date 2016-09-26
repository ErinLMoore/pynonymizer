Relies on Python packages `flask`, `flask-wtf`, `pygit2`. These can be install with pip.


to set up virtual environment, assuming python 3:
* `pyvenv flask`
* `flask/bin/pip3 install flask-restful`
* `flask/bin/pip3 install flask-wtf`
* `flask/bin/pip3 install requests`
* `flask/bin/pip3 install pygit2`

To run: `python3 run.py` will start the server.

(For Python 2, it should work with `virtualenv flask`, and then the rest of it
with the 3's taken out.)

With the server running, navigate in your browser to localhost:5000. The webpage should be ready for use.

A handy github repo you can use for testing is: `https://github.com/github/testrepo.git`

A new version of the anonymizer module with unit tests is planned.

The anonymizer module can be run as a standalone. use `python3 anonyizer.py <url-to-anonymize> <kata-description>`

NOTE: you will need an additional credentials file to run this. Please contact the creator directly if interested.
the credentials file goes in root to run the web app, or the same directory as 'anonymizer' to run it by itself.
