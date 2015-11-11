import re
from . import WORKSPACE, TAGS_REGEX
from git import Repo


class Repository:

    def __init__(self):
        if not WORKSPACE:
            raise Exception("No repository specified")

        repo_location = WORKSPACE
        self.repo = Repo(repo_location)

    def get_latest_tag(self, regex=TAGS_REGEX):
        if not regex:
            return sorted(self.tags, reverse=True)[0]
        tags = [tag for tag in filter(lambda tag: re.match(regex, tag.name), self.tags)]
        return sorted(tags, reverse=True)[0]

    def get_commits_since_tag(self, tag):
        commits = []
        for commit in self.repo.iter_commits():
            if tag.commit != commit:
                commits.append(commit)
            else:
                return commits

    @property
    def tags(self):
        return self.repo.tags

    @property
    def commits(self):
        return [commit for commit in self.repo.iter_commits()]

    @property
    def merged_commits(self):
        return [commit for commit in \
                filter(lambda commit: 'merge' in commit.message.lower(),
                       self.repo.iter_commits())]

