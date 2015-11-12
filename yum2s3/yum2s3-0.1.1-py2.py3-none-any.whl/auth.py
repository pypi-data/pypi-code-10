import click

__author__ = 'drews'

from boto3.session import Session


class Credentials(object):
    freeze_properties = ['region', 'aws_secret_access_key', 'aws_access_key_id', 'aws_session_token', 'profile', 'role']

    def __init__(self, region=None, aws_secret_access_key=None, aws_access_key_id=None, aws_session_token=None,
                 profile=None, role=None, role_session_name=None):

        self.region = region

        self.aws_secret_access_key = aws_secret_access_key
        self.aws_access_key_id = aws_access_key_id
        self.aws_session_token = aws_session_token
        self.profile = profile
        self.role = role
        self.role_session_name = role_session_name

        # Vars to store original creds, incase we assume a role
        self._freeze = {}

    def assume_role(self):
        if self.using_role():
            self._assume_role()
        else:
            raise ValueError("Could not find keys or profile")

    def freeze(self):
        """
        Take a snapshot fo the credentials and remember them.
        :return:
        """
        for property in self.freeze_properties:
            self._freeze[property] = getattr(self, property, None)

    def reset(self):
        """
        Reset Credentials object back to original state, pre any role assumptions.
        :return:
        """
        for property in self.freeze_properties:
            setattr(self, property, self._freeze[property])

    def create_session(self):

        session_credentials = {}

        # Get the credentials which can assume the role
        if self.has_keys():
            session_credentials['aws_access_key_id'] = self.aws_access_key_id
            session_credentials['aws_secret_access_key'] = self.aws_secret_access_key
            if self.has_session_keys():
                session_credentials['aws_session_token'] = self.aws_session_token
        elif self.has_profile():
            session_credentials['profile_name'] = self.profile

        default_region = self.region

        def build_session(region=default_region):
            session_credentials['region_name'] = region

            return Session(**session_credentials)

        return build_session

    def _assume_role(self):
        """
        Assume the new role, and store the old credentials
        :return:
        """
        # Remember the state
        self.freeze()

        # Assume the role
        session = self.create_session()
        credentials = session().client('sts').assume_role(
            RoleArn=self.role,
            RoleSessionName=self.role_session_name
        )

        self._orig_aws_access_key_id = self.aws_access_key_id
        self._orig_aws_secret_access_key = self.aws_secret_access_key
        self._orig_aws_session_token = self.aws_session_token

        self.aws_access_key_id = credentials['Credentials']['AccessKeyId']
        self.aws_secret_access_key = credentials['Credentials']['SecretAccessKey']
        self.aws_session_token = credentials['Credentials']['SessionToken']

    def has_keys(self):
        """
        Do we have key credentials?
        :return:
        """
        return (self.aws_access_key_id is not None) and \
               (self.aws_secret_access_key is not None)

    def has_session_keys(self):
        """
        Do we have temporal key credentials?
        :return:
        """
        return (self.aws_session_token is not None) and \
               self.has_keys()

    def has_profile(self):
        """
        Do we have profile credentials?
        :return:
        """
        return self.profile is not None

    def has_role(self):
        """
        Do we have a role to assume?
        :return:
        """
        return self.role is not None

    def using_role(self):
        """
        If we have a role and either a set of credentials or a profile, then we should assume the role
        :return:
        """
        return (
            self.has_role() and
            (self.has_keys() or self.has_profile())
        )


def validate_creds(aws_access_key_id, aws_secret_access_key, aws_session_token, profile, **kwargs):
    # 1 - Check if we have temporal keys
    if aws_session_token is not None:
        if (aws_secret_access_key is None) or (aws_access_key_id is None):
            raise click.BadParameter(
                "'--aws-session-token' requires '--aws-secret-access-key' and '--aws-access-key-id'")

    # 2 - Check if we have a profile
    if profile and (aws_access_key_id or aws_secret_access_key):
        raise click.BadParameter("You can not set both '--profile' and '--aws-secret-access-key'/'--aws-access-key-id'")

    # 3 - Check if we have keys
    if bool(aws_secret_access_key) != bool(aws_access_key_id):
        raise click.BadParameter("'Both '--aws-secret-access-key' and '--aws-access-key-id' must be provided.")
