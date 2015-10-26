from gcloud import datastore
from gcloud.datastore import SCOPE
from gcloud.datastore.connection import Connection

from oauth2client import client

def get_connection(client_email, private_key_string):
  svc_account_credentials = client.SignedJwtAssertionCredentials(
    service_account_name=client_email,
    private_key=private_key_string,
    scope=SCOPE)

  return Connection(credentials=svc_account_credentials)


def connect_to_dataset(dataset_id, client_email, private_key_string):
  connection = get_connection(client_email, private_key_string)
  datastore.set_default_connection(connection)
  datastore.set_default_dataset_id(dataset_id)

