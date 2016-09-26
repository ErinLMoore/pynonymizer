Relies on Python packages `flask`, `flask-wtf`, `pygit2`. These can be install with pip.


to set up virtual environment, assuming python 3:
* `pyvenv flask`
* `flask/bin/pip3 install -r requirements.txt`

Installing pygit2 requires a C library, it can be installed on a mac using
Homebrew: `brew install libgit2` and on
Debian using apt: `apt-get install libgit2-dev libffi`

To run: `python3 run.py` will start the server.

(For Python 2, it should work with `virtualenv flask`, and then the rest of it
with the 3's taken out.)

With the server running, navigate in your browser to localhost:5000. The webpage should be ready for use.

A new version of the anonymizer module with unit tests is planned.

NOTE: you will need an additional credentials file to run this. Please contact the creator directly if interested.
