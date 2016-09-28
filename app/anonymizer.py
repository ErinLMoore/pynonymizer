#!flask/bin/python3

import time
from datetime import date
import hashlib
import re
import os
import requests

git_username = git_password = git_token = 'not set'

if "pynonymizer_username" in os.environ:
    git_username = os.environ["pynonymizer_username"]
if "pynonymizer_password" in os.environ:
    git_password = os.environ["pynonymizer_password"]
if "pynonymizer_token" in os.environ:
    git_token = os.environ["pynonymizer_token"]

class Anonymizer(object):

    def __init__(self):
        pass

    def get_anonymous_name(self, description):
        current_time = str(time.time())
        epoch = current_time.encode()
        myhash = hashlib.md5(epoch).hexdigest()
        parsed_description = re.sub(r'\W', '-', description[:30])
        return parsed_description + "_" + str(date.today()) + "_" + myhash[:5]

    def create_github_repo(self, anonymous_name):
            dictToSend = {"name": anonymous_name}
            headers = {'Authorization': 'token {0}'.format(git_token)}
            response = requests.post('https://api.github.com/user/repos', json=dictToSend)
            print(response.json())
            return response.json()
