from request import Request
from listingRequest import ListingRequest
from officeRequest import OfficeRequest
from agentRequest import AgentRequest
from openHouseRequest import OpenHouseRequest
from assessmentRequest import AssessmentRequest
from transactionRequest import TransactionRequest
from parcelRequest import ParcelRequest
from vendorRequest import VendorRequest

BASE_URL = 'https://dev.rets.io/api/v1'

class Retsly:
  def __init__(self, token, vendor='test'):
    """
    Construct Retsly client

    Args:
      token (string):         access token
      vendor (string):        vendor ID

    """
    self.token = token
    self.vendor = vendor

  def getRequest(self, method, url, query):
    return Request(self, method, url, query)

  def getURL(self, resource):
    if resource == 'vendors':
      return '/'.join([BASE_URL, resource, self.vendor])
    else:      
      return '/'.join([BASE_URL, self.vendor, resource])

  def listings(self, query={}):
    return ListingRequest(self, query)

  def agents(self, query={}):
    return AgentRequest(self, query)

  def offices(self, query={}):
    return OfficeRequest(self, query)

  def openHouses(self, query={}):
    return OpenHouseRequest(self, query)

  def assessments(self, query={}):
    return AssessmentRequest(self, query)

  def transactions(self, query={}):
    return TransactionRequest(self, query)

  def parcels(self, query={}):
    return ParcelRequest(self, query)

  def vendors(self, query={}):
    return VendorRequest(self, query)
