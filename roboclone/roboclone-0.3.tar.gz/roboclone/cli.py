import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("remote_url", help="url of the remote git repository (https or ssh)")
    parser.add_argument("destination", nargs="?", help="directory to clone repository to")
    parser.add_argument("--gitargs", metavar="args", type=str, help="extra arguments for git")
    parser.add_argument("--force", nargs="?", help="write metadata files even if they already exist in the repo",
                        default=False, type=bool)
    return parser.parse_args()