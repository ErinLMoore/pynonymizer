#!flask/bin/python

from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource, reqparse

import pygit2 as git
import os
import shutil
import sys
import time
import datetime
import hashlib

import requests

from set_credentials import git_username, git_password, git_token

app = Flask(__name__)
api = Api(app)


def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f),
                                    os.path.join(dest, f),
                                    ignore)
    else:
        shutil.copyfile(src, dest)

def copy_directory_except_git(src, dst):
    ignore_patterns = ('.git/*', '.git')
    recursive_overwrite(src, dst, ignore=shutil.ignore_patterns(*ignore_patterns))

def delete_directory(src):
    shutil.rmtree(src, ignore_errors = True)

def create_github_repo(new_repo_name):
    dictToSend = {"name": new_repo_name}
    headers = {'Authorization': 'token {0}'.format(git_token)}
    res = requests.post('https://api.github.com/user/repos', json=dictToSend, headers=headers)
    print ('response from server:',res.text)
    dictFromServer = res.json()

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
        create_github_repo(anonymous_name)
        anonymizer = Anonymizer(request)
        anonymizer.anonymize(anonymous_name)

        return anonymizer.get_result()

    def get_anonymous_name(self, request):
        tmp = str(time.time())
        epoch = tmp.encode()
        myhash = hashlib.md5(epoch).hexdigest()
        parsed_description = request.description.replace(" ", "-")
        return parsed_description + "_" + str(datetime.date.today()) + "_" + myhash[:5]

class Anonymizer(object):
    def __init__(self, request):
        self.request = request
        self.result = {}
        self.username, self.password = git_username, git_password

    def anonymize(self, anonymous_name):
        cred= git.UserPass(self.username, self.password)
        callbacks = git.RemoteCallbacks(credentials = cred)
        git.clone_repository(self.request.url, "./local_copy", bare=False, callbacks = callbacks)
        original_repo = git.Repository("./local_copy/.git")

        git.init_repository("./anonymous_copy", flags = git.GIT_REPOSITORY_INIT_MKDIR)

        committer = git.Signature('Anonymous', 'anonymous@example.com')
        author = git.Signature('Anonymous', 'anonymous@example.com')
        parent = []
        counter = 0
        for commit in original_repo.walk(original_repo.head.target, git.GIT_SORT_TOPOLOGICAL):
            original_repo.checkout_tree(treeish = commit, strategy = git.GIT_CHECKOUT_ALLOW_CONFLICTS)
            copy_directory_except_git("./local_copy", "./anonymous_copy")
            copy_repo = git.Repository("./anonymous_copy/.git")

            tree = copy_repo.TreeBuilder().write()
            copy_repo.create_commit(
            'refs/heads/master', # the name of the reference to update
            author, committer, 'commit #' + str(counter),
            tree,
            parent
            )
            parent = [copy_repo.head.get_object().hex]
            counter += 1

        copy_repo.create_remote("origin", "https://github.com/{0}/{1}.git".format(self.username, anonymous_name))
        remote = copy_repo.remotes["origin"]
        remote.push(['refs/heads/master:refs/heads/master'], callbacks = callbacks)

        self.result = {'anonymous_url': anonymous_name, 'success': True}
        delete_directory("./local_copy")
        delete_directory("./anonymous_copy")

    def get_result(self):
        return self.result



api.add_resource(AnonymizeAPI, '/api/v1.0/anonymize', endpoint = 'anonymize')

if __name__ == '__main__':
    app.run(debug=True)
    sys.exit(0)
