#!flask/bin/python3

from flask import Flask
from flask import jsonify
from flask import render_template

import requests

import time
import datetime
import hashlib

from set_credentials import git_username, git_password, git_token

from .forms import UrlForm
from .anonymizer import Anonymizer
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    user = {'name': 'test'}  # fake user
    form = UrlForm()
    if form.validate_on_submit():
        dictToSend ={"url": form.submission_url.data, "description": form.description.data}
        anonymous_name = get_anonymous_name(dictToSend["description"])
        create_github_repo(anonymous_name)
        anonymizer = Anonymizer(dictToSend['url'], anonymous_name)
        anonymizer.anonymize()
        result = anonymizer.get_result()
        return render_template('result.html',
                                result=result)
    return render_template('index.html',
                           form=form,)

@app.route('/result', methods=['GET', 'PUT'])
def result():
    return render_template('result.html',
                            result = RESULT)

def create_github_repo(new_repo_name):
    dictToSend = {"name": new_repo_name}
    headers = {'Authorization': 'token {0}'.format(git_token)}
    res = requests.post('https://api.github.com/user/repos', json=dictToSend, headers=headers)
    print ('response from server:',res.text)
    dictFromServer = res.json()

def get_anonymous_name(description):
    tmp = str(time.time())
    epoch = tmp.encode()
    myhash = hashlib.md5(epoch).hexdigest()
    parsed_description = description.replace(" ", "-")
    return parsed_description + "_" + str(datetime.date.today()) + "_" + myhash[:5]
