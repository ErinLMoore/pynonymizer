#!flask/bin/python3

import pygit2 as git
import os
import shutil
import sys

import requests

import time
import datetime
import hashlib
#6b7c5759290649225bf21559b1431324

git_username = git_password = git_token = 'not set'

if "pynonymizer_username" in os.environ:
    git_username = os.environ["pynonymizer_username"]
if "pynonymizer_password" in os.environ:
    git_password = os.environ["pynonymizer_password"]
if "pynonymizer_token" in os.environ:
    git_token = os.environ["pynonymizer_token"]

class Anonymizer(object):
    def __init__(self, url_to_anonymize, description):
        self.url_to_anonymize = url_to_anonymize
        self.anonymous_name = self.get_anonymous_name(description)
        self.create_github_repo(self.anonymous_name)
        self.result = {}
        self.local_copy = "./local_copy"
        self.anonymous_copy = "./anonymous_copy"
        self.credentials = self.create_credential_callbacks()
        self.status_message = "Successful"

    def anonymize(self):
        try:
            original_repo = self.clone_a_repo()
            copy_repo = self.copy_repo_with_commits(original_repo)
        except:
            self.status_message = "error cloning and copying repo"
        self.anonymous_url = "https://github.com/{0}/{1}.git".format(self.username, self.anonymous_name)
        self.push_copy_repo(copy_repo)
        self.result = {'anonymous_url': self.anonymous_url, 'message': self.status_message}
        self.clean_up_directories()

    def get_result(self):
        return self.result

    def copy_repo_with_commits(self, original_repo):
        git.init_repository(self.anonymous_copy, flags = git.GIT_REPOSITORY_INIT_MKDIR)
        committer = git.Signature('Anonymous', 'anonymous@example.com')
        author = git.Signature('Anonymous', 'anonymous@example.com')
        parent = []
        for number, commit in enumerate(original_repo.walk(original_repo.head.target, git.GIT_SORT_TOPOLOGICAL)):
            original_repo.checkout_tree(treeish = commit, strategy = git.GIT_CHECKOUT_ALLOW_CONFLICTS)
            self.copy_directory_except_git(self.local_copy , self.anonymous_copy)
            copy_repo = git.Repository(self.anonymous_copy)
            index = copy_repo.index
            index.add_all()
            index.write()
            tree = index.write_tree()
            copy_repo.create_commit('refs/heads/master', author, committer,
            'commit #' + str(number),tree,parent)
            parent = [copy_repo.head.get_object().hex]
        return copy_repo

    def clone_a_repo(self):
        git.clone_repository(self.url_to_anonymize, self.local_copy , bare=False, callbacks = self.credentials)
        original_repo = git.Repository(self.local_copy)
        return original_repo

    def push_copy_repo(self, copy_repo):
        try:
            copy_repo.create_remote("origin", self.anonymous_url)
            copy_repo.remotes["origin"].push(['refs/heads/master:refs/heads/master'], callbacks = self.credentials)
        except:
            self.status_message = "error pushing repo"

    def create_credential_callbacks(self):
        self.username, self.password = git_username, git_password
        cred= git.UserPass(self.username, self.password)
        callbacks = git.RemoteCallbacks(credentials = cred)
        return callbacks

    def get_anonymous_name(self, description):
        tmp = str(time.time())
        epoch = tmp.encode()
        myhash = hashlib.md5(epoch).hexdigest()
        parsed_description = description.replace(" ", "-")
        return parsed_description + "_" + str(datetime.date.today()) + "_" + myhash[:5]

    def create_github_repo(self, anonymous_name):
        dictToSend = {"name": anonymous_name}
        headers = {'Authorization': 'token {0}'.format(git_token)}
        res = requests.post('https://api.github.com/user/repos', json=dictToSend, headers=headers)
        print ('response from server:',res.text)
        dictFromServer = res.json()

    def clean_up_directories(self):
        shutil.rmtree(self.local_copy , ignore_errors = True)
        shutil.rmtree(self.anonymous_copy , ignore_errors = True)

    def copy_directory_except_git(self, src, dst):
        ignore_patterns = ('.git/*', '.git')
        self.recursive_overwrite(src, dst, ignore=shutil.ignore_patterns(*ignore_patterns))

    def recursive_overwrite(self, src, dest, ignore=None):
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
                    self.recursive_overwrite(os.path.join(src, f),
                                        os.path.join(dest, f),
                                        ignore)
        else:
            shutil.copyfile(src, dest)

if __name__ == '__main__':
    anonymizer = Anonymizer(sys.argv[1], sys.argv[2])
    anonymizer.anonymize()
    result = anonymizer.get_result()
    print("\nAnonymous URL: {0} \n Status: {1}".format(result['anonymous_url'], result['message']))
