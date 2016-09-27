#!flask/bin/python3

import time
from datetime import date
import hashlib
import re

class Anonymizer(object):

    def __init__(self):
        pass

    def get_anonymous_name(self, description):
        current_time = str(time.time())
        epoch = current_time.encode()
        myhash = hashlib.md5(epoch).hexdigest()
        parsed_description = re.sub(r'\W', '-', description)
        return parsed_description + "_" + str(date.today()) + "_" + myhash[:5]

    def create_github_repo(self, anonymous_name):
        pass
