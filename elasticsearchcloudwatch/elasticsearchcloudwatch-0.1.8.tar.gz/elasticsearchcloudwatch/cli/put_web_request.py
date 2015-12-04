#!/usr/bin/env python

# Copyright 2015 Will Rubel
#
# Based on Python-Version of CloudWatch Monitoring Scripts for Linux -
# Copyright 2015 Oliver Siegmar. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from elasticsearchcloudwatch.cloud_watch_client import *
from elasticsearch import Elasticsearch

import argparse
from boto.ec2.cloudwatch import connect_to_region
from datetime import datetime, date, time
import os
import random
import re
import sys
import time
import ConfigParser
import get_web_request
from prettyprint import pp
import os
import subprocess
import boto3.session



# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


# Elasticsearch module if throwing warnings
# when not verifying SSL Certificates
import warnings
warnings.filterwarnings("ignore")



CLIENT_NAME = 'ElasticsearchCloudWatch-PutWebRequests'
FileCache.CLIENT_NAME = CLIENT_NAME
AWS_LIMIT_METRICS_SIZE = 20

Config = ConfigParser.ConfigParser()
config={}



######################################################
# Get the configuration inforamtion
######################################################




def __LINE__():
	try:
		raise Exception
	except:
		return sys.exc_info()[2].tb_frame.f_back.f_lineno


def ConfigSectionMap(section):
	dict1 = {}
	options = Config.options(section)
	for option in options:
		try:
			dict1[option] = Config.get(section, option)
			if dict1[option] == -1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1


def GetConfigData(query):

	Config.read("/etc/elasticsearchcloudwatch/escw.config")
	Config.sections()


	if ConfigSectionMap('AWS')['region']:
		config['aws_region'] = ConfigSectionMap("AWS")['region']
	else:
		print "must have a valid AWS region in the config file"
		exit


	if ConfigSectionMap(query)['metrics_category_name']:
		config['aws_metrics_category'] = ConfigSectionMap(query)['metrics_category_name']
	else:
		print "must have a valid AWS metrics category name"
		exit



	if ConfigSectionMap('General')['smtp_server']:
		config['smtp_server'] = ConfigSectionMap("General")['smtp_server']
	else:
		print "No alerts will not be email if you do not have a valid smtp server assigned"


	if ConfigSectionMap('General')['alert_email']:
		config['alert_email'] = ConfigSectionMap("General")['alert_email']
	else:
		print "No alerts will be emailed if you do not have a valid email address"


	if ConfigSectionMap('General')['from_address']:
		config['from_email'] = ConfigSectionMap("General")['from_address']
	else:
		print "No alerts will be emailed if you do not have a valid from email address assigned"


	if ConfigSectionMap('Proxy')['proxy_url']:
		config['proxy_url'] = ConfigSectionMap("Proxy")['proxy_url']
	else:
		config['proxy_url']='None'

	if ConfigSectionMap('Proxy')['proxy_port']:
		config['proxy_port'] = ConfigSectionMap("Proxy")['proxy_port']
	else:
		config['proxy_port']='None'


	if ConfigSectionMap('Proxy')['proxy_username']:
		config['proxy_username'] = ConfigSectionMap('Proxy')['proxy_username']
	else:
		config['proxy_username']='None'

	if ConfigSectionMap('Proxy')['proxy_password']:
		config['proxy_password'] = ConfigSectionMap('Proxy')['proxy_password']
	else:
		config['proxy_password']='None'


def config_parser():

	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description='''
  Submits the web request from elasticsearch to Amazon CloudWatch.''', epilog='''

Examples

 To perform a simple test run

  ./put_web_request.py --host-ip 127.0.0.1 --verbose


 To set a five-minute cron schedule to report web request
 to CloudWatch

  */5 * * * * ~/elasticsearchcloudwatch/put_web_request.py  --from-cron


For more information on how to use this utility, see project home on BitBucket:
https://rubelw@bitbucket.org/rubelw/elasticsearchcloudwatch.git
	''')



	parser.add_argument('--version',
		action='store_true',
		help='Displays the version number and exits.')


	parser.add_argument('--from-cron',
		action='store_true',
		help='Specifies the script is running from cron.')


	parser.add_argument('--verbose',
		action='store_true',
		help='Displays details of what the script is doing.')

	parser.add_argument('--query',
		required=True,
		help='The query name from the config file.')



	return parser


def alert(subject,msg):

	if from_email and alert_email and smtp_server:
		msg = MIMEMultipart()
		msg['Subject'] = str(subject)
		msg['From'] = from_email
		msg['To'] =alert_email
		body = str(msg)
		msg.attach(MIMEText(body, 'plain'))


		# Send the message via our own SMTP server, but don't include the
		# envelope header.
		s = smtplib.SMTP(smtp_server)
		s.sendmail(from_email, alert_email, msg.as_string('test'))
		s.quit()



def main():
	parser = config_parser()

	# exit with help, because no args specified
	#if len(sys.argv) == 1:
	#	parser.print_help()
	#	return 1

	args = parser.parse_args()

	if args.verbose:
		print 'in main() - line: '+str(__LINE__())


	if args.version:
		print CLIENT_NAME + ' version ' + VERSION
		return 0


	GetConfigData(args.query)

	try:


		# avoid a storm of calls at the beginning of a minute
		if args.from_cron:

			if args.verbose:
				print "from cron - sleeping for random seconds - line: "+str(__LINE__())

			time.sleep(random.randint(0, 19))

		if args.verbose:
			print 'Working in verbose mode'
			print 'Boto-Version: ' + boto.__version__
			print 'Elasticsearch-Version: ' + str(elasticsearch.__version__)
			print 'AWS Region: '+str(config['aws_region'])
			print '-----------------------------------'
			print 'Getting data from elasticsearch'


		# Call the get web to collect the data
		results = get_web_request.main()

		# Get the results from the elasticsearch buckets
		dict={}


		if not results:
			print "List is empty"
		else:
			for s in results:
				dict[str(s['key'])]= str(s['doc_count'])

			if args.verbose:
				print 'aws metrics category: '+config['aws_metrics_category']
				print 'aws region: '+config['aws_region']
				print 'proxy_url:'+str(config['proxy_url'])
				print 'proxy_port'+str(config['proxy_port'])



			proxies = {}

			if config['proxy_url'] != 'None' and config['proxy_port'] != 'None':
				proxies['http'] = str(config['proxy_url'] + ':' + str(config['proxy_port']))
				proxies['https'] = str(config['proxy_url'] + ':' + str(config['proxy_port']))

				# Setting environmental variables for cron
				os.environ['HTTP_PROXY'] = proxies['http']
				os.environ['http_proxy'] = proxies['http']
				os.environ['HTTPS_PROXY'] = proxies['https']
				os.environ['https_proxy'] = proxies['http']



			# TODO Turn on debugging for boto if verbose
			# TODO add timeout
			list = []
			my_date= datetime.utcnow()

			for key,value in dict.iteritems():
				temp = {}
				temp['MetricName']= str(key)
				temp['Timestamp']= my_date
				print('my value is: '+str(value))
				temp['Value'] = int(value)
				temp['Unit'] = 'Count'
				list.append(temp)

			if args.verbose:
				print('Namespace: '+str(config['aws_metrics_category']))
				print(list)



			session = boto3.session.Session(region_name=str(config['aws_region']))
			cw_client = session.client('cloudwatch')
			response = cw_client.put_metric_data(
					Namespace=str(config['aws_metrics_category']),
					MetricData= list
			)



			if not response:
				raise ValueError('Could not send data to CloudWatch - '
				'use --verbose for more information')

			if args.verbose:
				pp(response)






	except Exception as e:
		log_error(str(e), args.from_cron)
		return 1

	return 0


if __name__ == '__main__':
	sys.exit(main())
