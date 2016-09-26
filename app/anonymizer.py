#!flask/bin/python3

import pygit2 as git
import os
import shutil
import sys

from set_credentials import git_username, git_password, git_token

class Anonymizer(object):
    def __init__(self, url_to_anonymize, anonymous_name):
        self.url_to_anonymize = url_to_anonymize
        self.anonymous_name = anonymous_name
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
