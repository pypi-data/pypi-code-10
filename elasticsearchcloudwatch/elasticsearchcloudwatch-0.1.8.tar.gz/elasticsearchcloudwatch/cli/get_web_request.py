#!/usr/bin/env python

# Copyright 2015 Will Rubel
#
# Based on Perl-Version of CloudWatch Monitoring Scripts for Linux -
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
from elasticsearch import Elasticsearch, RequestsHttpConnection
from datetime import datetime
import argparse
from prettyprint import pp
import ConfigParser
import requests
import sys
import os
import subprocess


# Elasticsearch module if throwing warnings
# when not verifying SSL Certificates
import warnings
warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings()


CLIENT_NAME = 'ElasticSearchCloudWatch-GetWebRequest'
FileCache.CLIENT_NAME = CLIENT_NAME
Config = ConfigParser.ConfigParser()
config={}

#####################################################
# Utilities
#####################################################

# For debugging
def __LINE__():
	try:
		raise Exception
	except:
		return sys.exc_info()[2].tb_frame.f_back.f_lineno



######################################################
# Get the configuration information
######################################################


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


# Pull the elasticsearch and AWS config data, and query information based-on
# the section named for the query in this parameter
def GetConfigData(query):
	Config.read("/etc/elasticsearchcloudwatch/escw.config")
	Config.sections()

	if ConfigSectionMap(query)['index']:
		config['wr_index'] = ConfigSectionMap(query)['index']
	else:
		print "Must have an index"
		exit


	if ConfigSectionMap(query)['doc_type']:
		config['wr_doc_type'] = ConfigSectionMap(query)['doc_type']
	else:
		print "Must have an document type"
		exit


	if ConfigSectionMap(query)['query']:
		config['wr_query'] = ConfigSectionMap(query)['query']
	else:
		print "Must have an query string"
		exit


	if ConfigSectionMap(query)['query_type']:
		config['wr_query_type'] = ConfigSectionMap(query)['query_type']
	else:
		print "Must have an query type"
		exit



	if ConfigSectionMap('Elasticsearch')['es_protocol']:
		config['es_protocol'] = ConfigSectionMap('Elasticsearch')['es_protocol']
	else:
		print "Must have a protocl in the config file"
		exit

	if ConfigSectionMap("Elasticsearch")['es_url']:
		config['es_url'] = ConfigSectionMap("Elasticsearch")['es_url']
	else:
		print 'Must have a valid url for the elasticsearch server in the config file'
		exit

	if ConfigSectionMap('Elasticsearch')['es_port']:
		config['es_port'] = ConfigSectionMap("Elasticsearch")['es_port']
	else:
		print 'Must have a valid port for the elasticsearch server in the config file'
		exit

	if ConfigSectionMap('Elasticsearch')['es_username']:
		config['es_username'] = ConfigSectionMap('Elasticsearch')['es_username']
	else:
		config['es_username']='None'

	if ConfigSectionMap('Elasticsearch')['es_password']:
		config['es_password'] = ConfigSectionMap('Elasticsearch')['es_password']
	else:
		config['es_password']='None'


	if ConfigSectionMap('Elasticsearch')['es_suffix']:
		config['es_suffix'] = ConfigSectionMap('Elasticsearch')['es_suffix']
	else:
		config['es_suffix']='None'


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
	Queries Elasticsearch for web statistics.
''', epilog='''
For more information on how to use this utility, see project home on BitBucket:
https://rubelw@bitbucket.org/rubelw/elasticsearchcloudwatch.git
''')



	parser.add_argument('--verbose',
						action='store_true',
						help='Displays details of what the script is doing.')

	parser.add_argument('--version',
						action='store_true',
						help='Displays the version number and exits.')

	parser.add_argument('--query',
						required=True,
						help='The query name from the config file.')

	parser.add_argument('--from-cron',
						action='store_true',
						help='Displays details of what the script is doing.')

	return parser




# Query elastic search
def print_web_request(protocol,host_ip, host_port, idx, username, password,  verbose, proxy_ip, proxy_port, doc_t,proxy_user,proxy_pass,query,es_suffix):

	global response

	if verbose:
		print "making request to elasticsearch - line: "+str(__LINE__())


	if username != 'None' and password != 'None':
		# using basic authentication
		if verbose:
			print 'has username and password - using basic authentication - line: '+str(__LINE__())

		proxies = {}

		if proxy_ip != 'None' and proxy_port != 'None':
			proxies['http'] = str(proxy_ip + ':' + str(proxy_port))
			proxies['https'] = str(proxy_ip + ':' + str(proxy_port))

			# Setting environmental variables for cron
			os.environ['HTTP_PROXY'] = proxies['http']
			os.environ['http_proxy'] = proxies['http']
			os.environ['HTTPS_PROXY'] = proxies['https']
			os.environ['https_proxy'] = proxies['http']

			if verbose:
				print "using a proxy - line:"+str(__LINE__())


			if proxy_user != 'None' and proxy_pass != 'None':
				if verbose:
					print 'proxy server is using authentication - line: '+str(__LINE__())

				if protocol == 'http' or protocol == 'HTTP':
					if verbose:
						print 'using http protocol - line: '+str(__LINE__())

					if es_suffix != 'None':
						if verbose:
							print "ES url has a suffix - line: "+ __LINE__()

						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=False,
							verify_certs=False
						)

					else:
						if verbose:
							print "ES url does not have a suffix - line: "+str(__LINE__())

						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=False,
							verify_certs=False
						)



					response = es.search(index=idx, doc_type=doc_t, body=query)

					if verbose:
						print 'made it here - line: '+str(__LINE__())
						pp(response)

					#return("%d" % response['hits']['total'])
					return response['aggregations']['response']['buckets']



				else:   # assuming https for now - need to fix
					if verbose:
						print 'using https protocol - line: '+str(__LINE__())


					if es_suffix != 'None':
						if verbose:
							print "ES url has a suffix - line: "+str(__LINE__())

						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=True,
							verify_certs=False
						)

					else:
						if verbose:
							print "ES url does not have a suffix - line: "+str(__LINE__())
						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=True,
							verify_certs=False
						)


					response = es.search(index=idx, doc_type=doc_t, body=query)

					if verbose:
						print 'made it here - line: '+str(__LINE__())
						pp(response)

					#return("%d" % response['hits']['total'])
					return response['aggregations']['response']['buckets']


			else:
				if verbose:
					print 'proxy server is not using authentication- line: '+str(__LINE__())


				if protocol == 'http' or protocol == 'HTTP':
					if verbose:
						print 'using http protocol - line: '+str(__LINE__())

					if es_suffix != 'None':
						if verbose:
							print "ES url has a suffix - line: "+str(__LINE__())

						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=False,
							verify_certs=False
						)

					else:
						if verbose:
							print "ES url does not have a suffix - line: "+str(__LINE__())

						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=False,
							verify_certs=False
						)


					response = es.search(index=idx, doc_type=doc_t, body=query)

					if verbose:
						print 'made it here - line: '+str(__LINE__())
						pp(response)

					#return("%d" % response['hits']['total'])
					return response['aggregations']['response']['buckets']

				else:
					if verbose:
						print 'using https protocol - line: '+str(__LINE__())
						print "\t"+'protocol is:'+str(protocol)
						print "\t"+'host ip is:'+str(host_ip)
						print "\t"+'host_port is:'+str(host_port)
						print "\t"+'query is: '+str(query)
						print "\t"+'index is: '+str(idx)
						print "\t"+'doc type is:'+str(doc_t)



					if es_suffix != 'None':
						if verbose:
							print "ES url has a suffix - line: "+ str(__LINE__())
							print "\t"+'suffix is: '+str(es_suffix)

						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=True,
							verify_certs=False
						)

					else:
						if verbose:
							print "ES url does not have a suffix - line: "+str(__LINE__())

						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=True,
							verify_certs=False
						)


					response = es.search(index=idx, body=query)



					if verbose:
						print 'made it here - line: '+str(__LINE__())
						pp(response)

					#return("%d" % response['hits']['total'])
					return response['aggregations']['response']['buckets']

		else:

                        if verbose:
                                print "not using a proxy - line:"+str(__LINE__())


                        if protocol == 'http' or protocol == 'HTTP':
                        	if verbose:
                                	print 'using http protocol - line: '+str(__LINE__())

                                if es_suffix != 'None':
                                	if verbose:
                                        	print "ES url has a suffix - line: "+str(__LINE__())

                                        es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
                                                connection_class=RequestsHttpConnection,
                                                http_auth=(username, password),
                                                use_ssl=False,
                                                verify_certs=False
                                        )

                                else:
                                        if verbose:
                                                print "ES url does not have a suffix - line: "+str(__LINE__())

                                        es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
                                                connection_class=RequestsHttpConnection,
                                                http_auth=(username, password),
                                                use_ssl=False,
                                                verify_certs=False
                                        )


                                response = es.search(index=idx, doc_type=doc_t, body=query)

                                if verbose:
                                        print 'made it here - line: '+str(__LINE__())
                                        pp(response)

                                #return("%d" % response['hits']['total'])
                                return response['aggregations']['response']['buckets']

                        else:
                                if verbose:
                                        print 'using https protocol - line: '+str(__LINE__())
                                        print "\t"+'protocol is:'+str(protocol)
                                        print "\t"+'host ip is:'+str(host_ip)
                                        print "\t"+'host_port is:'+str(host_port)
                                        print "\t"+'query is: '+str(query)
                                        print "\t"+'index is: '+str(idx)
                                        print "\t"+'doc type is:'+str(doc_t)



                                if es_suffix != 'None':
                                        if verbose:
                                                print "ES url has a suffix - line: "+ str(__LINE__())
                                                print "\t"+'suffix is: '+str(es_suffix)


                                        es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
                                                connection_class=RequestsHttpConnection,
                                                http_auth=(username, password),
                                                use_ssl=True,
                                                verify_certs=False
                                        )

                                else:
                                        if verbose:
                                                print "ES url does not have a suffix - line: "+str(__LINE__())

                                        es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
                                                connection_class=RequestsHttpConnection,
                                                http_auth=(username, password),
                                                use_ssl=True,
                                                verify_certs=False
                                        )


                                response = es.search(index=idx, body=query)

                                if verbose:
                                        print 'made it here - line: '+str(__LINE__())
                                        pp(response)

                                #return("%d" % response['hits']['total'])
                                return response['aggregations']['response']['buckets']


	else:
		# not using basic authentication
		if verbose:
			print 'does not have username and password - not using basic authentication- line: '+str(__LINE__())

		proxies = {}

		if proxy_ip != 'None' and proxy_port != 'None':
			if verbose:
				print 'we are using a proxy - line: '+str(__LINE__())

			proxies['http'] = proxy_ip + ':' + str(proxy_port),
			proxies['https'] = proxy_ip + ':' + str(proxy_port)

			# Setting environmental variables for cron
			os.environ['HTTP_PROXY'] = proxies['http'] # visible in this process + all children
			os.environ['http_proxy'] = proxies['http'] # visible in this process + all children
			os.environ['HTTPS_PROXY'] = proxies['https'] # visible in this process + all children
			os.environ['https_proxy'] = proxies['http'] # visible in this process + all children


			if proxy_user != 'None' and proxy_pass != 'None':
				if verbose:
					print 'proxy server is using authentication- line: '+str(__LINE__())

				if protocol == 'http' or protocol == 'HTTP':

					if verbose:
						print 'using http protocol - line: '+str(__LINE__())


					if es_suffix != 'None':
						if verbose:
							print "ES url has a suffix- line: "+str(__LINE__())




						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=False,
							verify_certs=False
						)

					else:
						if verbose:
							print "ES url does not have a suffix - line: "+str(__LINE__())

						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=False,
							verify_certs=False
						)



					response = es.search(index=idx, doc_type=doc_t, body=query)

					if verbose:
						print 'made it here - line: '+str(__LINE__())
						pp(response)

					#return("%d" % response['hits']['total'])
					return response['aggregations']['response']['buckets']

				else:  # Assuming https protocol
					if verbose:
						print 'using https protocol - line: '+str(__LINE__())


					if es_suffix != 'None':
						if verbose:
							print "ES url has a suffix - line: "+str(__LINE__())

						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=True,
							verify_certs=False
						)

					else:
						if verbose:
							print "ES url does not have a suffix - line: "+str(__LINE__())

						es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=True,
							verify_certs=False
						)


					response = es.search(index=idx, doc_type=doc_t, body=query)

					if verbose:
						print 'made it here - line: '+str(__LINE__())
						pp(response)

					#return("%d" % response['hits']['total'])
					return response['aggregations']['response']['buckets']


			else:
				if verbose:
					print 'proxy server is not using authentication - line: '+str(__LINE__())


				if es_suffix != 'None':
					if verbose:
						print "ES url has a suffix - line: "+str(__LINE__())

					es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=True,
							verify_certs=False
					)

				else:
					if verbose:
						print "ES url does not have a suffix - line: "+str(__LINE__())

					es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
							proxies=proxies,
							connection_class=RequestsHttpConnection,
							http_auth=(username, password),
							use_ssl=True,
							verify_certs=False
					)



				response = es.search(index=idx, doc_type=doc_t, body=query)

				if verbose:
					print 'made it here - line: '+str(__LINE__())
					pp(response)

				#return("%d" % response['hits']['total'])
				return response['aggregations']['response']['buckets']

		else:
			if verbose:
				print 'we are not using a proxy - line: '+str(__LINE__())


			if protocol == 'http' or protocol == 'HTTP':

				if verbose:
					print 'using http protocol - line: '+str(__LINE__())


				if es_suffix != 'None':
					if verbose:
						print "ES url has a suffix - line: "+str(__LINE__())

					es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
							connection_class=RequestsHttpConnection,
							use_ssl=False,
					)

				else:
					if verbose:
						print "ES url does not have a suffix - line: "+str(__LINE__())

					es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
							connection_class=RequestsHttpConnection,
							use_ssl=False,
					)



				response = es.search(index=idx, doc_type=doc_t, body=query)

				if verbose:
					print 'made it here - line: '+str(__LINE__())
					pp(response)

				#return("%d" % response['hits']['total'])
				return response['aggregations']['response']['buckets']


			else:  # Assuming https protocol
				if verbose:
					print 'using https protocol - line: '+str(__LINE__())



				if es_suffix != 'None':
					if verbose:
						print "ES url has a suffix - line: "+str(__LINE__())

					es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)+'/'+es_suffix+'/'],
							connection_class=RequestsHttpConnection,
							use_ssl=True,
					)

				else:
					if verbose:
						print "ES url does not have a suffix - line: "+str(__LINE__())
					es = Elasticsearch([protocol+'://' + host_ip + ':' + str(host_port)],
							connection_class=RequestsHttpConnection,
							use_ssl=True,
					)



				response = es.search(index=idx, doc_type=doc_t, body=query)

				if verbose:
					print 'made it here - line: '+str(__LINE__())
					pp(response)

				return response['aggregations']['response']['buckets']



def main():


	parser = config_parser()



	args = parser.parse_args()

	if args.version:
		print CLIENT_NAME + ' version ' + VERSION
		return 0

	if args.verbose:
		print args


	GetConfigData(args.query)


	try:

		results = print_web_request(config['es_protocol'],config['es_url'], config['es_port'], config['wr_index'], config['es_username'], config['es_password'],
						  args.verbose, config['proxy_url'], config['proxy_port'], config['wr_doc_type'],config['proxy_username'],config['proxy_password'],config['wr_query'],config['es_suffix'])

		if sys._getframe().f_back.f_code.co_name == '<module>':
			pp(results)
		else:
			return results

	except Exception as e:
		log_error(str(e), False)
		return 1

	return 0


if __name__ == '__main__':
	sys.exit(main())

