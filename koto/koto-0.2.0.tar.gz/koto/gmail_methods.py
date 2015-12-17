from __future__ import print_function

import httplib2
import os
import os.path

import base64
import email

import datetime


from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools

from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
	Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')

	store = oauth2client.file.Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		# if flags:
		# 	credentials = tools.run_flow(flow, store, flags)
		# else: # Needed only for compatibility with Python 2.6
		credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError, error:
        print ('An error occurred: %s' % error)

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, format="raw").execute()

    # print ('Message snippet: %s' % message['snippet'])
    return message
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)

#returns the datetime a certain message ID was sent
def getDate(service, msgID):
	#get internalDate in epoch ms:
	date = GetMessage(service, "me", msgID)['internalDate']

	#convert to float
	fdate = float(date)

	#convert to timestamp and then datetime
	return (datetime.datetime.fromtimestamp(fdate/1000.0))

#returns the number of days that passed since given date
def daysSince(date):
	days = date - datetime.datetime.today()
	sdays = str(days).split()

	#take abs value of day value (must convert from str -> int -> str)
	sdays[0] = str(abs(int(sdays[0])))

	if (sdays[0] == "1"):
		return (sdays[0] + " day")
	else:
		return (sdays[0] + " days")

#returns ID of latest email from specific email address
def getLatest(service, user_id, query=''):
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query, maxResults=1).execute()
    return(response['messages'][0])

    # if 'message' in response:
    # 	message.extend(response['message'])

    # messages = []
    # if 'messages' in response:
    #   messages.extend(response['messages'])

    # while 'nextPageToken' in response:
    #   page_token = response['nextPageToken']
    #   response = service.users().messages().list(userId=user_id, q=query,
    #                                      pageToken=page_token).execute()
    #   messages.extend(response['messages'])

    # return messages[0]
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)

#returns text body parsed out of 'full' message from g.GetMessage()
def extractBody(rawMessage):
	msg_str = base64.urlsafe_b64decode(rawMessage['raw'].encode('UTF-8'))
	msg = email.message_from_string(msg_str)	
	for part in msg.walk():
		msg.get_payload()
		if part.get_content_type() == 'text/plain':
			# mytext = base64.urlsafe_b64decode(part.get_payload().encode('UTF-8'))
			mytext = part.get_payload()
			# print part.get_payload()
			return (mytext)	

class _DeHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.__text = []

	def handle_data(self, data):
		text = data.strip()
		if len(text) > 0:
			text = sub('[ \t\r\n]+', ' ', text)
			self.__text.append(text + ' ')

	def handle_starttag(self, tag, attrs):
		if tag == 'p':
			self.__text.append('\n\n')
		elif tag == 'br':
			self.__text.append('\n')

	def handle_startendtag(self, tag, attrs):
		if tag == 'br':
			self.__text.append('\n\n')

	def text(self):
		return ''.join(self.__text).strip()

def dehtml(text):
	try:
		parser = _DeHTMLParser()
		parser.feed(text)
		parser.close()
		return parser.text()
	except:
		print_exc(file=stderr)
		return text