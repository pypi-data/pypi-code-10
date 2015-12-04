from colorama import Fore
from git import *

class GitObj(object):

    def __init__(self, entry):
        self.entry = self.check_entry(entry)
        self.git_object = self.get_repo_from_entry(entry)
        self.current_status = self.return_current_status()
        self.all_commits = len(list(self.git_object.iter_commits()))
        self.commits_to_push = self.return_nb_commits_to_push()
        self.untracked_files = len(self.git_object.untracked_files)
        self.ref = self.git_object.head.reference

    def __del__(self):
        pass

    def __str__(self):
        status_color = Fore.RED if self.current_status == "DIRTY" else Fore.GREEN
        entry_from_home = "~/{0}".format("/".join(self.entry.split("/")[3:]))
        if not self.current_status == "TO PUSH":
            return "\t[{0}] {1} -- {2} commit(s) -- {3} untracked file(s) -- \033[1m branch {4} \033[0m".format(status_color + self.current_status + Fore.RESET, entry_from_home, self.all_commits, self.untracked_files, self.ref)
        else:
            return "\t[{0}] {1} -- {2} commit(s) to push -- {3} untracked file(s) -- \033[1m branch {4} \033[0m".format(Fore.BLUE + self.current_status + Fore.RESET, entry_from_home, self.commits_to_push, self.untracked_files, self.ref)

    def check_entry(self, entry):
        if entry[-1] == '\n':
            entry = entry[:-1]
        return entry

    def get_repo_from_entry(self, entry):
        return Repo(self.entry)

    def return_current_status(self):
        if self.git_object.is_dirty():
            return "DIRTY"
        elif not "Your branch is up-to-date" in self.git_object.git.status():
            return "TO PUSH"
        else:
            return "CLEAN"

    def return_nb_commits_to_push(self):
        git_status = self.git_object.git.status()
        if self.current_status == "TO PUSH":
            if "Your branch is ahead of" in git_status:
                split_git_status_0 = git_status.split("commit")[0] or git_status.split("commits")[0]
                split_git_status_0 = split_git_status_0.split('by')[1]
                return int(split_git_status_0)
            else:
                self.current_status = "CLEAN"
                return 0
