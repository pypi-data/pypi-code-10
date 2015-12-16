

# (c) Head In Cloud BVBA, Belgium
# http://www.headincloud.be

from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
import logging
from codedeploy_monitor.exceptions import ConfigException


logger = logging.getLogger(__name__)

USAGE = (
    "\n"
    "codedeploy_monitor create-deployment [arguments]\n"
    "  (to create a new deployment and start monitoring it.)\n"
    "\n"
    "codedeploy_monitor monitor-deployment [arguments]\n"
    "  (to monitor a deployment that has been already created.)\n"
    "\n"
    "To see help text, you can run:\n"
    "\n"
    "  codedeploy_monitor create-deployment --help\n"
    "  codedeploy_monitor monitor-deployment --help\n"

)

USAGE_CREATE = (
    "\n"
    "codedeploy_monitor create-deployment [arguments]\n"
    "\n"
)

USAGE_MONITOR = (
    "\n"
    "codedeploy_monitor monitor-deployment [arguments]\n"
    "\n"
)


class ConfigParser:

    app_config = None
    parser = None

    def __init__(self, app_config):
        self.app_config = app_config
        self.parser = ArgumentParser(formatter_class=RawTextHelpFormatter, usage=USAGE, add_help=False)
        action_parser = self.parser.add_subparsers(dest="app_action")
        creation_parser = action_parser.add_parser('create-deployment', help=SUPPRESS, formatter_class=RawTextHelpFormatter, usage=USAGE_CREATE)
        monitor_parser = action_parser.add_parser('monitor-deployment', help=SUPPRESS, formatter_class=RawTextHelpFormatter, usage=USAGE_MONITOR)

        # Parser for creation of new deployment + monitoring
        creation_parser.add_argument("--application-name", help="The name of an existing AWS CodeDeploy application associated with the applicable IAM user or AWS account.", required=True)
        creation_parser.add_argument("--deployment-group", help="The deployment group's name.", required=True)
        creation_parser.add_argument("--deployment-config-name", help="The name of an existing deployment configuration associated with the applicable IAM user or AWS account.", default="")
        creation_parser.add_argument("--description", help="A comment about the deployment.", default="")
        creation_parser.add_argument("--sns-topic", help="Send notifications to specified SNS topic. (NOT IMPLEMENTED YET)")

        origin_exclusive_group = creation_parser.add_mutually_exclusive_group()
        origin_exclusive_group.add_argument("--s3-location", help="bucket=string,key=string,bundleType=tar|tgz|zip,version=string,eTag=string")
        origin_exclusive_group.add_argument("--github-location", help="repository=string,commitId=string")

        # Parser for monitor-only operation
        monitor_parser.add_argument("--deployment-id", help="Id of deployment you want to monitor.", required=True)
        monitor_parser.add_argument("--sns-topic", help="Send notifications to specified SNS topic.")

    def print_help(self):
        self.parser.print_help()

    def parse(self, command_args):
        args = self.parser.parse_args(command_args)
        logger.debug("argparse results: {}".format(args))
        setattr(self.app_config, "app_action", args.app_action)
        logger.debug("Action to perform: {}.".format(args.app_action))
        if args.app_action == "monitor-deployment":
            setattr(self.app_config, "deployment_id", args.deployment_id)
        else:
            logger.debug("Parsing CodeDeploy arguments:")
            for entry in ("application_name", "deployment_group","deployment_config_name", "description"):
                logger.debug("{} = {}".format(entry, getattr(args, entry)))
                setattr(self.app_config, entry, getattr(args, entry))
            if args.s3_location:
                logger.debug("Parsing S3 arguments:")
                setattr(self.app_config, "type", "S3")
                s3_params = dict(item.split("=") for item in args.s3_location.split(","))
                for entry in ("bucket", "key", "bundleType"):
                    logger.debug("{} = {}".format(entry, s3_params[entry]))
                    if entry not in s3_params:
                        raise ConfigException("An argument is missing in the S3 location string: '{}'.".format(entry))

                setattr(self.app_config, "s3_params", s3_params)

            elif args.github_location:
                logger.debug("Parsing GitHub arguments:")
                setattr(self.app_config, "type", "GitHub")
                github_params = dict(item.split("=") for item in args.github_location.split(","))
                for entry in ("repository", "commitId"):
                    logger.debug("{} = {}".format(entry, github_params[entry]))
                    if entry not in github_params:
                        raise ConfigException("An argument is missing in the GitHub location string: '{}'.".format(entry))

                setattr(self.app_config, "github_params", )

            else:
                raise ConfigException("Either --s3-location or --github-location must be specified.")
