
# (c) Head In Cloud BVBA, Belgium
# http://www.headincloud.be

import logging
import boto3
from codedeploy_monitor.exceptions import DeployException

logger = logging.getLogger(__name__)


class CodeDeploy:

    client = None
    app_config = None

    def __init__(self, app_config):
        self.app_config = app_config

    def connect(self):
        self.client = boto3.client('codedeploy')

    def create_deployment(self):
        parameters = dict()
        parameters['applicationName'] = getattr(self.app_config, "application_name")
        parameters['deploymentGroupName'] = getattr(self.app_config, "deployment_group")
        if self.app_config.type == "S3":
            parameters['revision'] = {
                'revisionType': 'S3',
                's3Location': self.app_config.s3_params
            }
        elif self.app_config.type == "GitHub":
            parameters['revision'] = {
                'revisionType': 'GitHub',
                'gitHubLocation': self.app_config.github_params
            }

        deployment_config_name = getattr(self.app_config, "deployment_config_name", "")
        if deployment_config_name:
            parameters['deploymentConfigName'] = deployment_config_name

        description = getattr(self.app_config, "description", "")
        if description:
            parameters['description'] = description

        parameters['ignoreApplicationStopFailures'] = False

        try:
            response = self.client.create_deployment(**parameters)
            return response['deploymentId']
        except Exception as e:
            raise DeployException(e)

    def get_deployment_status(self, deployment_id):
        try:
            logger.debug("Trying to get status for deployment id {}".format(deployment_id))
            response = self.client.get_deployment(deploymentId=deployment_id)
            logger.debug("Response received: {}.".format(response))
            return response['deploymentInfo']['status']
        except Exception as e:
            raise DeployException(e)




