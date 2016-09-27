#!flask/bin/python3

import time
from datetime import date
import hashlib

class Anonymizer(object):

    def __init__(self):
        pass

    def get_anonymous_name(description):
        current_time = str(time.time())
        epoch = current_time.encode()
        myhash = hashlib.md5(epoch).hexdigest()
        parsed_description = description.replace(" ", "-")
        return parsed_description + "_" + str(datetime.date.today()) + "_" + myhash[:5]
