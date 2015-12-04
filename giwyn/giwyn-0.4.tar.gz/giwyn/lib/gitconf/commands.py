import giwyn.lib.settings.settings
from git import *

def list_git_projects():
    print("List of git projects:")
    #end="" -> avoid last '\n' character
    for git_object in giwyn.lib.settings.settings.GIT_OBJECTS:
        print(git_object)

def push_ready_projects():
    print("Repository to push...")
    any_repo_to_push = False
    for git_project in giwyn.lib.settings.settings.GIT_OBJECTS:
        if git_project.current_status == "TO PUSH":
            print("Pushing {0} in the current branch...".format(git_project.entry))
            git_project.git_object.remote().push()
            any_repo_to_push = True
    if not any_repo_to_push:
        print("There is no repository to push yet!")

def pull_ready_projects():
    print("Repository to pull...")
    any_repo_to_pull = False
    for git_project in giwyn.lib.settings.settings.GIT_OBJECTS:
        if git_project.current_status == "CLEAN":
            print("Try to pull {0}, from the current branch...".format(git_project.entry))
            #Pull from origin
            if git_project.git_object.remotes != []:
                git_project.git_object.remotes.origin.pull()
                any_repo_to_pull = True
    if not any_repo_to_pull:
        print("There is no repository to pull yet!")
