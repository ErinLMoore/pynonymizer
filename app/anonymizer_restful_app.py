#!flask/bin/python3

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import flash
from flask import redirect
from flask_restful import Api, Resource, reqparse

import requests

import time
import datetime
import hashlib

from set_credentials import git_username, git_password, git_token

from .forms import UrlForm
from .anonymizer import Anonymizer
from app import app
api = Api(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    user = {'name': 'test'}  # fake user

    form = UrlForm()
    if form.validate_on_submit():
        flash('here is url="%s", &desc=%s' %
            (form.submission_url.data, str(form.description.data)))
        return redirect('/index')

    return render_template('index.html',
                           user=user,
                           form=form)

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
        anonymous_name = self.get_anonymous_name(request)
        try:
            self.create_github_repo(anonymous_name)
            anonymizer = Anonymizer(request.url, anonymous_name)
            anonymizer.anonymize()
            return anonymizer.get_result()
        except:
            return {'anonymous_url': anonymous_name, 'status_message': 'error creating repo'}

    def create_github_repo(self, new_repo_name):
        dictToSend = {"name": new_repo_name}
        headers = {'Authorization': 'token {0}'.format(git_token)}
        res = requests.post('https://api.github.com/user/repos', json=dictToSend, headers=headers)
        print ('response from server:',res.text)
        dictFromServer = res.json()

    def get_anonymous_name(self, request):
        tmp = str(time.time())
        epoch = tmp.encode()
        myhash = hashlib.md5(epoch).hexdigest()
        parsed_description = request.description.replace(" ", "-")
        return parsed_description + "_" + str(datetime.date.today()) + "_" + myhash[:5]



api.add_resource(AnonymizeAPI, '/api/v1.0/anonymize', endpoint = 'anonymize')
