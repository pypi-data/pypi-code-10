import os

from untestable.i_o.console_io import ConsoleIO
from untestable.bitbucket_app import BitbucketApp
from untestable.i_o.file_based_credential_persistence import FileBasedCredentialPersistence
from untestable.flow.simple_credentials_collection_flow import SimpleCredentialsCollectionFlow
from untestable.i_o.rest_bitbucket_client import RestBitBucketClient
from untestable.commands.g_user_command import GUserCommand
from untestable.commands.g_user_repos_command import GUserReposCommand


_IO = ConsoleIO()
_CREDS = FileBasedCredentialPersistence(os.path.join(os.path.expanduser("~"), ".untestable"))
_FLOW = SimpleCredentialsCollectionFlow(_IO, _CREDS)
_BBCLIENT = RestBitBucketClient()
_GUSER = GUserCommand(_IO, _FLOW, _BBCLIENT)
_GUSERREPOS = GUserReposCommand(_IO, _FLOW, _BBCLIENT)
APP = BitbucketApp(_IO, _GUSER, _GUSERREPOS)
