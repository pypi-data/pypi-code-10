
# (c) Head In Cloud BVBA, Belgium
# http://www.headincloud.be

import sys
import logging
import time
from codedeploy_monitor.config import AppConfig
from codedeploy_monitor.exceptions import ConfigException, DeployException
from codedeploy_monitor.config_parser import ConfigParser
from codedeploy_monitor.deploy_utils import CodeDeploy


logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    app_config = AppConfig()
    config_parser = ConfigParser(app_config)
    # show help if no parameters are given
    if len(sys.argv) == 1:
        logger.debug("No parameters supplied. printing help")
        config_parser.print_help()

    # start

    try:
        logger.debug("Parsing command-line options.")
        config_parser.parse(sys.argv[1:])
    except ConfigException as e:
        logger.error("An error occured while parsing the command-line parameters:")
        logger.error("(ERROR): {}".format(e))
        sys.exit(1)

    code_deploy = CodeDeploy(app_config)
    code_deploy.connect()

    if app_config.app_action == "create-deployment":
        try:
            logger.info("Creating deployment...")
            deployment_id = code_deploy.create_deployment()
            logger.info("Deployment {} created.".format(deployment_id))
        except DeployException as e:
            logger.error("An error occurred while creating a new deployment:")
            logger.error("(ERROR): {}".format(e))
            sys.exit(1)

    elif app_config.app_action == "monitor-deployment":
        deployment_id = app_config.deployment_id

    # Start monitoring deployment here.
    status = code_deploy.get_deployment_status(deployment_id)
    prev_status = ""
    logging.info("Current status of deployment is: {}.".format(status))
    logging.info("Polling every 5 seconds for status changes...")
    while status not in ('Succeeded', 'Failed', 'Stopped'):
        time.sleep(5)
        prev_status = status
        status = code_deploy.get_deployment_status(deployment_id)
        if status != prev_status:
            logging.info("Status changed to: {}".format(status))

    if status == "Failed" or status == "Stopped":
        logging.error("An error occured during deployment. Last state: {}.".format(status))
        exit(1)

    elif status == "Succeeded":
        logging.info("Deployment finished successfully. Last state: {}.".format(status))
        exit(0)

if __name__ == "__main__":
    main()
