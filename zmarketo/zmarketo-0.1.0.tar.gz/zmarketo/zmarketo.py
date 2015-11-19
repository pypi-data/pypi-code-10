import json
import requests
import urllib
from datetime import datetime, timedelta

# TODO:
# Better api return values (raw funcs, and formatted funcs)
	# Mostly just:
	# {skipped: }
	# And single vs. bulk funcs.
# Docstrings and generate docs.
# Add all the Marketo rest functions
# Tests for each method
# More elegant handling of the marketo api check decorator. (Magic mock.)
# Handle unicode better (import unicode literal?)
# Possible future settings:
# Optional:
# isDev: bool (False)
# shouldCache: bool (False)

class MarketoInvalidInputException(Exception):
	def _makeResponseStr(self, message):
		return u"Marketo Api has invalid input: {}: ".format(message)

	def __init__(self, message):
		super(MarketoInvalidInputException, self).__init__(self._makeResponseStr(message))
		self.message = message

	def __str__(self):
		return self._makeResponseStr(self.message)

class BadRequest(Exception):
	def _makeResponseStr(self, code, body):
		return u"Request was bad. Response code: {}, Response body {}".format(code, body)

	def __init__(self, responseCode, responseBody):
		super(BadRequest, self).__init__(self._makeResponseStr(responseCode, responseBody))
		self.code = responseCode
		self.body = responseBody

	def __str__(self):
		return _makeResponse(self.code, self.body)

class MarketoApiError(Exception):
	ERROR_CODES = {
		'413': 'Payload exceeded 1MB limit.',
		'414': ('URI of the request exceeded 8k. The request should be retried as a POST with param _method=GET in the URL,'
					' and the rest of the querystring in the body of the request.'),
		'601': 'An Access Token parameter was included in the request, but the value was not a valid access token.',
		'602': 'The Access Token included in the call is no longer valid due to expiration.',
		'603': ('Authentication is successful but user doesn\'t have sufficient permission to call this API. '
					'Additional permissions may need to be assigned to the user role.'),
		'604': 'The request was running for too long, or exceeded the time-out period specified in the header of the call.',
		'605': 'GET is not supported for syncLead, POST must be used.',
		'606': 'The number of calls in the past 20 seconds was greater than 100',
		'607': 'Number of calls today exceeded the subscription\'s quota.  The default subscription quota is 10,000/day.',
		'608': 'API Temporarily Unavailable',
		'609': 'The body included in the request is not valid JSON.',
		'610': 'The URI in the call did not match a REST API resource type.  This is often due to an incorrectly spelled or incorrectly formatted request URI',
		'611': 'All unhandled exceptions',
		'612': ('If you see this error, add a content type header specifying JSON format to your request. For example, try using "content type: application/json".'
					'Please see this (http://stackoverflow.com/questions/28181325/why-invalid-content-type) StackOverflow question for more details.'),
		'613': 'The multipart content of the POST was not formatted correctly',
		'701': 'The reported field must not be empty in the request',
		'702': 'No records matched the given search parameters',
		'703': 'A beta feature that has not been in enabled in a user\'s subscription',
		'704': 'A date was specified that was not in the correct format',
		'709': 'The call cannot be fulfilled because it violates a requirement to create up update an asset, e.g. trying to create an email without a template.',
		'710': 'The specified parent folder could not be found',
		'711': 'The specified folder was not of the correct type to fulfill the request',
		'1001': 'Error is generated whenever parameter value has type mismatch. For example string value specified for integer parameter.',
		'1002': 'Error is generated when required parameter is missing from the request',
		'1003': 'Ex: When proper action (createOnly, createOrUpdate ..etc) not specified.',
		'1004': 'For syncLead, when action is "updateOnly" and if lead is not found',
		'1005': 'For syncLead, when action is "createOnly" and if lead already exists',
		'1006': 'An included field in the call is not a valid field.',
		'1007': 'Multiple leads match the lookup criteria.  Updates can only be performed when the key matches a single record',
		'1008': 'The user for the custom service does not have access to a workspace with the partition where the record exists.',
		'1010': 'The specified record already exists in a separate lead partition.',
		'1011': 'When lookup field or filterType specified with unsupported standard fields (ex: firstName, lastName ..etc)',
		'1013': 'Get object (list, campaign ..etc) by id will return this error code',
		'1014': 'Failed to create Object (list, ..etc)',
		'1015': 'The designated lead is not a member of the target list',
		'1016': 'There are too many imports queued.  A maximum of 10 is allowed',
		'1017': 'Creation failed because the record already exists',
		'1018': 'The action could not be carried out, because the instance has a native CRM integration enabled.',
		'1019': 'The target list is already being imported to',
		'1020': 'The subscription has reached the alotted uses of cloneToProgramName in Schedule Program for the day',
		'1021': 'Company update not allowed during syncLead',
		'1022': 'Delete is not allowed when an object is in use by another object',
	}

	def makeResponseStr(self, errors, requestArgs):
		responseStr = u"Marketo API Error for {}.".format(requestArgs if requestArgs else '()')
		for error in errors:
			errorCode = error.get('code')
			description = self.ERROR_CODES.get(errorCode, 'No description for this code')
			responseStr += u"\nError code: {}. message: {}. Error description: {}\n".format(errorCode, error.get('message'), description)

		return responseStr

	def __init__(self, errors, requestArgs):
		super(MarketoApiError, self).__init__(self.makeResponseStr(errors, requestArgs))
		self.errors = errors
		self.requestArgs = requestArgs

	def __str__(self):
		return repr(self.makeResponseStr(self.errors, self.requestArgs))


def handleRequestResponse(func):
	def responseHandler(*args, **kwargs):
		def handleResponse(statusCode, responseData, retryCount=0):
			self = args[0]

			if statusCode != 200:
				raise BadRequest(statusCode, responseData)
			elif responseData['success']:
				return responseData['result']
			else:
				errors = responseData["errors"]

				for error in errors:
					if error.get('code') == '602' and retryCount < 3:
						self.tokenParams = {'access_token': self._getMarketoAccessToken()}
						retryCount += 1
						return handleResponse(*func(*args, **kwargs), retryCount=retryCount)

				raise MarketoApiError(errors, args)

		return handleResponse(*func(*args, **kwargs))
	return responseHandler

class MarketoRest(object):
	URL_ENDPOINT = "https://180-gfh-982.mktorest.com"
	IDENTITY = "https://180-GFH-982.mktorest.com/identity"

	def __init__(self, client_id, client_secret, session=None):
		if not session:
			session = requests.Session()

		self.client_id = client_id
		self.client_secret = client_secret

		session.headers.update({'content-type': 'application/json;charset=UTF-8'})
		self.requestSession = session
		self.tokenParams = {'access_token': self._getMarketoAccessToken()}

	def _getMarketoAccessToken(self):
		"""
		Marketo Docs for getting access code
		http://developers.marketo.com/documentation/rest/authentication/
		"""

		authQuery = {
			'grant_type': 'client_credentials',
			'client_id': self.client_id,
			'client_secret': self.client_secret,
		}

		marketoAuthUrl = '{0}{1}'.format(self.URL_ENDPOINT, '/identity/oauth/token')
		authResponse = self.requestSession.get(marketoAuthUrl, params=authQuery)
		token = authResponse.json().get('access_token')

		if authResponse.status_code != 200 or not token:
			raise BadRequest(authResponse.status_code, authResponse.content)

		return token

	def getPaginationApiToken(self, date=None):
		getPaginationApiTokenEndpoint = '/rest/v1/activities/pagingtoken.json'

		if not date:
			date = datetime.utcnow() - timedelta(minutes=30)

		requestData = {'sinceDatetime': date.strftime("%Y-%m-%dT%H:%M-%S:00")}
		requestData.update(self.tokenParams)
		resp = self.requestSession.get('{0}{1}'.format(self.URL_ENDPOINT, getPaginationApiTokenEndpoint), params=requestData)

		if resp.status_code != 200:
			raise BadRequest(resp.status_code, resp.content)

		return resp.json()

	@handleRequestResponse
	def describeLead(self):
		"""
		Marketo Docs for describing leads:
		http://developers.marketo.com/documentation/rest/describe/
		"""

		url = u'{0}{1}'.format(self.URL_ENDPOINT, '/rest/v1/leads/describe.json')
		resp = self.requestSession.get(url, params=self.tokenParams)
		print 'RESPONSE: {}'.format(resp)

		return (resp.status_code, resp.json())

	def displayRestNames(self, displayName=None):
		"""
		Displays fields on leads in a human readable format. Can filter on display name to get the field name.
		"""

		restNames = []
		for lead in self.describeLead():
			if 'rest' in lead:
				restNames.append((lead['displayName'], lead['rest']['name'], lead['dataType'], lead.get('length', 'N/A')))

		if displayName:
			restNames = [lead for lead in restNames if lead[0] == displayName]

		for restName in restNames:
			print u"Display: {}, API: {}, Data Type: {} Length: {}".format(restName[0],  restName[1], restName[2], restName[3])

	@handleRequestResponse
	def get_leads_by_filter_type(self, filterType, filterValues, fields=None, batchSize=300, nextPageToken=None):
		"""
		Docs at http://developers.marketo.com/documentation/rest/get-multiple-leads-by-filter-type
		"""

		getLeadEndpoint = '/rest/v1/leads.json'
		urlParams = {'filterType': filterType, 'batchSize': batchSize}
		urlParams.update(self.tokenParams)

		if fields:
			urlParams['fields'] = ','.join(fields)

		if nextPageToken:
			urlParams['nextPageToken'] = nextPageToken

		if type(filterValues) == list:
			urlParams['filterValues'] = ','.join(filterValues)
		else:
			urlParams['filterValues'] = filterValues

		resp = self.requestSession.get('{0}{1}'.format(self.URL_ENDPOINT, getLeadEndpoint), params=urlParams)

		return (resp.status_code, resp.json())

	@handleRequestResponse
	def create_or_update_leads(self, leads, lookupField='email', action='createOrUpdate', asyncProcessing=False, partitionName=None):
		"""
		Marketo Docs for creating/updating leads http://developers.marketo.com/documentation/rest/createupdate-leads/
		"""
		postData = {
			'lookupField': lookupField,
			'input': leads,
			'action': action,
			'asyncProcessing': asyncProcessing
		}

		if partitionName:
			postData.update({'partitionName': partitionName})

		resp = self.requestSession.post(
			'{0}{1}?{2}'.format(self.URL_ENDPOINT, '/rest/v1/leads.json', urllib.urlencode(self.tokenParams)),
			data=json.dumps(postData)
		)

		return (resp.status_code, resp.json())

	@handleRequestResponse
	def add_leads_to_list(self, leadIds, listId):
		"""
		Lead Ids is expected to be [{'id': ...}, ...]
		Marketo Docs for adding leads to list http://developers.marketo.com/documentation/rest/add-leads-to-list/
		"""
		resp = self.requestSession.post(
			'{0}{1}?{2}'.format(self.URL_ENDPOINT, '/rest/v1/lists/{0}/leads.json'.format(listId), urllib.urlencode(self.tokenParams)),
			data=json.dumps({'input': leadIds})
		)

		return (resp.status_code, resp.json())

	##################################################################################
	# Convenience Functions. Not in api but used for common operations.              #
	##################################################################################

	def create_or_update_lead(self, lead, lookupField='email', action='createOrUpdate', asyncProcessing=False, partitionName=None):
		"""
		Creates or updates a single lead.
		"""
		results = self.create_or_update_leads([lead], lookupField, action, asyncProcessing, partitionName)

		if not results:
			raise MarketoInvalidInputException("uploaded lead's should not be empty.")

		return results[0]

	def add_lead_to_list(self, leadId, listId):
		"""
		Takes single lead id and adds it to the list.
		"""
		results = self.add_leads_to_list([{'id': leadId}], listId)

		if not results:
			raise MarketoInvalidInputException("uploaded lead's should not be empty.")

		return results[0]
