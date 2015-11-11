#!/usr/bin/env python
from __future__ import print_function
from lambda_local import Lambda
from deploy import LambdaDeploy
import argparse
import os

parser = argparse.ArgumentParser(description="Run an AWS Lambda function locally.")
subparsers = parser.add_subparsers()

# Parser for the run command
parser_run = subparsers.add_parser("run", help="Runs the local lambda function.")
parser_run.add_argument("file", type=str,
                    help="the file containing your lambda function.")
parser_run.add_argument("-e", "--event", type=str, default=None,
                    help="the json containing the event data. Default None.")
parser_run.add_argument("-n", "--name", type=str, default="handler",
                    help="the name of the method lambda should call. Default 'handler'")

# Parser for the deploy command
parser_deploy = subparsers.add_parser("deploy", help="Deploys the lambda function to S3 as a zip. MUST BE run from within the directory containing the lambda function.")
parser_deploy.add_argument("s3_bucket", type=str,
                    help="the s3 bucket location. IE: s3://my_bucket/my_subfolder/")
parser_deploy.add_argument("-n", "--name", type=str, default=None,
                    help="Name of zipped file. Defaults to 'my_lambda_function'.")

def main():
    args = parser.parse_args()
    args = vars(args)
    
    # Decide if runnning or deploying
    if "s3_bucket" in args:
        d = LambdaDeploy(os.getcwd(), args["s3_bucket"], args["name"])
        d.deploy()
    elif "file" in args:
        test_lambda = Lambda(args["file"], args["event"], args["name"])
        print(test_lambda.run())
    else:
        print("Invalid arguments encountered. Please use -h to see help.")

if __name__ == '__main__':
    main()
    