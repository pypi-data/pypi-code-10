import boto3

kms = boto3.client('kms')
default_keyname = 'alias/credkeep'
