#!flask/bin/python

from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource, reqparse

import pygit2 as git
import os
import shutil
import sys

app = Flask(__name__)
api = Api(app)

def copy_directory_except_git(src, dst):
    ignore_patterns = ('.git/*', '.git')
    shutil.copytree(src, dst, symlinks=False,  ignore=shutil.ignore_patterns(*ignore_patterns))

class AnonymizeAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type = str, required = True,
            help = 'No url provided', location = 'json')
        self.reqparse.add_argument('description', type = str, default = '',
            location = 'json')
        super(AnonymizeAPI, self).__init__()

    def post(self):
        request = self.reqparse.parse_args()

        anonymizer = Anonymizer(request)
        anonymizer.anonymize()

        return anonymizer.get_result()

class Anonymizer(object):
    def __init__(self, request):
        self.request = request
        self.result = {}

    def anonymize(self):
        cred= git.UserPass("Anonymous-Katas", "v~LD%%r*j!~VT94L")
        callbacks = pygit2.RemoteCallbacks(credentials = cred)
        git.clone_repository(self.request.url, "./local_copy", bare=False, callbacks = callbacks)
        #self.result = {'anonymous_url': 'shasdflk', 'success': True}

    def get_result(self):
        return self.result



api.add_resource(AnonymizeAPI, '/api/v1.0/anonymize', endpoint = 'anonymize')

if __name__ == '__main__':
    app.run(debug=True)
    sys.exit(0)
