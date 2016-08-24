#!flask/bin/python

from flask import Flask
from flask import jsonify 
from flask_restful import Api, Resource, reqparse

import pygit2 as git
import os
import shutil

app = Flask(__name__)
api = Api(app)

def copy_directory_except_one_subdirectory(src, dst, ignore):
    for root, dirs, files in os.walk(src):
        if ignore not in root:
            for f in files:
                shutil.copy(os.path.join(root, f), os.path.join(root, f).replace(src, dst, 1))        
            for d in dirs:
                if d != ignore:
                    os.makedirs(os.path.join(root, d).replace(src, dst, 1))

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
        self.result = {'anonymous_url': 'shasdflk', 'success': True}

    def get_result(self):
        return self.result



api.add_resource(AnonymizeAPI, '/api/v1.0/anonymize', endpoint = 'anonymize')

if __name__ == '__main__':
    app.run(debug=True)
