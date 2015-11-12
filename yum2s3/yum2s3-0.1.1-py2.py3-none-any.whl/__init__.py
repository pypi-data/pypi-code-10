from yum2s3 import auth
from yum2s3.syncer import Syncer

__author__ = 'drews'

import click


@click.command()
@click.option('--aws-access-key-id', envvar='AWS_ACCESS_KEY_ID', help='AWS access key')
@click.option('--aws-secret-access-key', envvar='AWS_SECRET_ACCESS_KEY',
              help='Access and secret key variables override credentials stored in credential and config files',
              default=None)
@click.option('--aws-session-token', envvar='AWS_SESSION_TOKEN',
              help='A session token is only required if you are using temporary security credentials.', default=None)
@click.option('--region', envvar='AWS_DEFAULT_REGION',
              help='This variable overrides the default region of the in-use profile, if set.')
@click.option('--profile', envvar='AWS_DEFAULT_PROFILE',
              help='This can be the name of a profile stored in a credential or config file, or default to use the default profile.',
              default=None)
@click.option('--role', help='Role to assume')
@click.option('--role-session-name', help='If you have assigned a role, set a RoleSessionName')
@click.argument('repo_config')
@click.argument('s3_target')
def run(repo_config, s3_target, **kwargs):
    """
    Greets a person and prints a message of the day.
    """
    auth.validate_creds(**kwargs)
    session = auth.Credentials(**kwargs).create_session()

    Syncer(
        repos=repo_config,
        s3target=s3_target,
        session=session
    ).load_repos().run()
