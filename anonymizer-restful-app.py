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
        from set_credentials import git_username, git_password
        self.username, self.password = git_username, git_password

    def anonymize(self):
        cred= git.UserPass(self.username, self.password)
        callbacks = git.RemoteCallbacks(credentials = cred)
        git.clone_repository(self.request.url, "./local_copy", bare=False, callbacks = callbacks)
        original_repo = git.Repository("./local_copy/.git")

        git.init_repository("./anonymous_copy", flags = git.GIT_REPOSITORY_INIT_MKDIR)

        parent = []
        for commit in original_repo.walk(original_repo.head.target, git.GIT_SORT_TOPOLOGICAL):
            print (commit.tree_id)
            original_repo.checkout_tree(treeish = commit, strategy = git.GIT_CHECKOUT_ALLOW_CONFLICTS)
            copy_directory_except_git("./local_copy", "./anonymous_copy")
            copy_repo = git.Repository("./anonymous_copy/.git")
            author = git.Signature('Alice Author', 'alice@authors.tld')
            committer = git.Signature('Cecil Committer', 'cecil@committers.tld')
            tree = copy_repo.TreeBuilder().write()
            copy_repo.create_commit(
            'refs/heads/master', # the name of the reference to update
            author, committer, 'one line commit message\n\ndetailed commit message',
            tree, # binary string representing the tree object ID
            parent
            )
            parent = [copy_repo.head.get_object().hex]
            #raise GitError(message)
        delete_directory("./local_copy")
        self.result = {'anonymous_url': 'shasdflk', 'success': True}

    def get_result(self):
        return self.result



api.add_resource(AnonymizeAPI, '/api/v1.0/anonymize', endpoint = 'anonymize')

if __name__ == '__main__':
    app.run(debug=True)
    sys.exit(0)
