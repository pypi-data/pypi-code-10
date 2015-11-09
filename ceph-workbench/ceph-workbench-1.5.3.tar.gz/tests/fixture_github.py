# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2015 <contact@redhat.com>
#
# Author: Loic Dachary <loic@dachary.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from ceph_workbench import util
from ceph_workbench import wbgithub
import github
import shutil
import tempfile

GITHUB = {
    'token': '2f9990ef48be2255267f6a9a394389e24cc10e31',
    'username': 'ceph-workbench',
    'repo': 'testrepo',
    'password': 'Oktowyic8',
}


class FixtureGitHub(object):

    def setUp(self):
        self.argv = [
            '--github-token', GITHUB['token'],
            '--github-repo', GITHUB['username'] + '/' + GITHUB['repo'],
        ]
        self.github = wbgithub.WBGitHub.factory(self.argv).open()
        self.remove_project()
        self.add_project()
        return self

    def tearDown(self):
        self.remove_project()

    def project_exists(self, name):
        for repo in self.github.g.user('repos').get():
            if repo['name'] == name:
                return True
        return False

    def add_project(self):
        r = self.github.g.user('repos').post(
            name=GITHUB['repo'],
            auto_init=True)
        assert r['full_name'] == GITHUB['username'] + '/' + GITHUB['repo']
        while not self.project_exists(GITHUB['repo']):
            pass

    def remove_project(self):
        if self.project_exists(GITHUB['repo']):
            try:
                self.github.g.repos(GITHUB['username'] + '/' +
                                    GITHUB['repo']).delete()
            except github.ApiNotFoundError:
                pass  # this may happen because removal is asynchronous
        while self.project_exists(GITHUB['repo']):
            pass

    def clone_url(self):
        t = "http://{username}:{password}@github.com/{username}/{repo}"
        return t.format(username=GITHUB['username'],
                        password=GITHUB['password'],
                        repo=GITHUB['repo'])

    def pull_request(self, name, body, base):
        d = tempfile.mkdtemp()
        util.sh("""
        git clone {url} {d}
        cd {d}
        git branch wip-{name} origin/{base}
        git checkout wip-{name}
        echo a > file-{name}.txt ; git add file-{name}.txt ; git commit -m 'm' file-{name}.txt # noqa
        git push origin wip-{name}
        """.format(url=self.clone_url(),
                   d=d,
                   name=name,
                   base=base))
        shutil.rmtree(d)
        repos = self.github.g.repos(GITHUB['username'])(GITHUB['repo'])
        pr = repos.pulls().post(
            title=name,
            base=base,
            body=body,
            head='wip-' + name)
        return pr['number']
