from pre_commit.file_classifier.classifier import classify
from pre_commit import git

def identify(args):
    path = args.path
    # TODO: check if in the git repo first
    print(classify(path, git.guess_git_type_for_file(path)))
