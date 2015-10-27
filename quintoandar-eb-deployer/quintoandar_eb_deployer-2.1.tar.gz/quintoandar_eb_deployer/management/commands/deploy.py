from django.core.management.base import BaseCommand
from optparse import make_option
from quintoandar_eb_deployer.app_settings import *
import subprocess
import os
import urllib2
import json

class Command(BaseCommand):

	file_path = os.path.dirname(os.path.realpath(__file__))
	file_name = file_path + '/_awsElasticbeanstalkPush.py'

	option_list = BaseCommand.option_list + (
					make_option('--environment', '-e',
						help='Set deployment environment; Values: (%s)' % "|".join(EB_DEPLOYER_SETTINGS.get("envs").keys())
					),
					make_option('--commit', '-c',
						help='Commit hash to rollback to'
					),
					make_option('--skip-static',
						action='store_true',
						default=False,
						help='Skip pushing static files'
					),
					make_option('--access-key','-k',
						help='AWS EB ACCESS_KEY'
					),
					make_option('--secret-key','-s',
						help='AWS EB SECRET_KEY'
					),
				)
  
	def handle(self, *args, **options):
		
		ENV = options.get('environment')

		if not ENV or (ENV not in EB_DEPLOYER_SETTINGS.get("envs").keys()):
			print 'Especify an environment: -e (%s)' % "|".join(EB_DEPLOYER_SETTINGS.get("envs").keys())
			return

		COMMIT = options.get('commit')
		SKIP_STATIC = options.get('skip_static')
		ACCESS_KEY = options.get('access_key')
		SECRET_KEY = options.get('secret_key')
		REGION = EB_DEPLOYER_SETTINGS.get("envs").get(ENV).get("REGION")
		ENVIRONMENT_NAME = EB_DEPLOYER_SETTINGS.get("envs").get(ENV).get("ENVIRONMENT_NAME")
		APPLICATION_NAME = EB_DEPLOYER_SETTINGS.get("envs").get(ENV).get("APPLICATION_NAME")
		STATIC_FILES_SCRIPT = EB_DEPLOYER_SETTINGS.get("envs").get(ENV).get("STATIC_FILES_SCRIPT")
		SLACK_URL = EB_DEPLOYER_SETTINGS.get("SLACK_URL")
		
		if SLACK_URL:
			username = subprocess.check_output('git config user.name', shell=True).rstrip('\n')
			commitmessage = subprocess.check_output('git log -1 --pretty=%B', shell=True)
			reponame = subprocess.check_output('remote=$(git config --get branch.master.remote);url=$(git config --get remote.$remote.url);basename=$(basename "$url" .git);echo $basename', shell=True).rstrip('\n')
			slack_message = {
				"fallback": username + ' is deploying ' + reponame + ' to ' + ENV + ': ' + commitmessage,
				"color": "#00ADEF", 
				"pretext": username + ' is deploying ' + reponame + ' to ' + ENV,
				"fields": [ 
					{ 
						"value": "Commit: " + commitmessage, 
						"short": False
					} 
				] 
			} 
			
			urllib2.build_opener(urllib2.HTTPCookieProcessor()).open(SLACK_URL, '%s' % json.dumps(slack_message));

		print 'Deploying to: ' + ENV + '...'

		eb_update_command = [
			'python', 
			self.file_name, 
			'--access-key=' + ACCESS_KEY,
			'--secret-key=' + SECRET_KEY,
			'--region=' + REGION,
			'--environment-name=' + ENVIRONMENT_NAME,
			'--application-name=' + APPLICATION_NAME
		]
		if COMMIT:
			eb_update_command.append('--commit='+COMMIT)
		
		self.cmd(eb_update_command)

		if STATIC_FILES_SCRIPT:
			if SKIP_STATIC:
				print 'Skiping static files script...'
			else:
				print 'Running static files script...'		
				os.system("./%s %s %s %s" % (STATIC_FILES_SCRIPT, ENV, ACCESS_KEY, SECRET_KEY))

		print 'Done deploying to: ' + ENV + '!'

	def cmd(self, command, shell=False):

		os.system(" ".join(command))
