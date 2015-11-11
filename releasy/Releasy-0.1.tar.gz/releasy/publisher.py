import json
from releasy.repo import Repository
from releasy.log import PrettyLog


class Publisher:

    def __init__(self):
        self.repo = Repository()
        commits = self.repo.get_commits_since_tag(self.repo.get_latest_tag())
        self.log = PrettyLog(commits)


class JsonPublisher(Publisher):

    def publish(self):
        return json.dumps(self.log.detailed_log_map)
