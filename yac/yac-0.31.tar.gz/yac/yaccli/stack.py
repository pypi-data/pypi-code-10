import argparse
from yac.yaccli.lib.stack import create_stack

def main():

    parser = argparse.ArgumentParser('Print a stack for an Atlassian application via cloudformation')
    # required args
    parser.add_argument('app',  help='name of the app to build stack for', 
                                choices=['jira','crowd','confluence','bamboo','stash','hipchat'])
    parser.add_argument('env',  help='the env', 
                                choices=['dev', 'stage', 'prod','archive'])

    # optional
    # store_true allows user to not pass a value (default to true, false, etc.)
    parser.add_argument('-c','--create',  
                        help='create a new stack rather than updating existing (defaults to false)', 
                        action='store_true')

    args = parser.parse_args()

    return create_stack()