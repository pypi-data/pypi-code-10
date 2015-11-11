import os

WORKSPACE = os.environ.get('WORKSPACE')

TAGS_REGEX = os.environ.get('TAGS_REGEX')

PROJECT_TICKET_REGEX = os.environ.get('PROJECT_TICKET_REGEX')

JIRA_BROWSE_URL = os.environ.get('JIRA_BROWSE_URL', "https://jira.made.com/browse/")

PROJECT_GITHUB_URL = os.environ.get('PROJECT_GITHUB_URL')
