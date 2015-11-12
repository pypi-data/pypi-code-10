import glob
import os
import pyum
from os import path

__author__ = 'drews'


class Syncer(object):
    def __init__(self, repos, s3target, session):
        self.repos_path = path.abspath(path.expanduser(repos))
        self.repos = []
        self.s3target = s3target
        self.session = session

    def load_repos(self):
        if os.path.isdir(self.repos_path):
            for file in glob.glob("{0}/*.repo".format(self.repos_path)):
                repo = pyum.RepoFile(file)
                repo.set_yum_variables(
                    releasever='7',
                    basearch='x86_64'
                )

                self.repos.append(repo)
        else:
            repo = pyum.RepoFile(self.repos_path)
            repo.set_yum_variables(
                releasever='7',
                basearch='x86_64'
            )
            self.repos = [repo]
        return self

    def run(self):
        pass
