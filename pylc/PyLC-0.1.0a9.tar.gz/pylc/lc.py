# The MIT License (MIT)
# 
# Copyright (c) 2015 Benjamin Morrise
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import urllib, urllib2, json

from resources import AccountResource, LoanResource

class LendingClubAPI:

  API_VERSION = 'v1'
  API_URL = 'https://api.lendingclub.com/api/'
  api_key = ''
  investor_id = ''
  resources = []  

  def __init__(self, api_key, investor_id, debug=False):
    self.api_key = api_key
    self.investor_id = investor_id
    self.debug = debug
    self._register_resources()

    if self.debug == True:
      print "!!======= DEBUG ENABLED =======!!"

  def _register_resources(self):
    self._add_resource(AccountResource(self))
    self._add_resource(LoanResource(self))

  def _add_resource(self, resource):
    resource_name = resource.__class__.__name__
    try:
      name_index = resource_name.index("Resource")
      resource_name = resource_name[0:name_index].lower()
      self.resources.append(resource_name)
      setattr(self, resource_name, resource)
    except Exception:
      raise ValueError("Invalid resource name: %s" % resource_name)

  def get_resources(self):
    return self.resources

  def _call(self, params, query_string=None, data=None):
    path = ""
    for param in params:
      path += param + "/"
    url = self.API_URL + "investor/%s/%s" % (self.API_VERSION, path)
    if query_string is not None:
      url += "?" + urllib.urlencode(query_string)
    
    headers = { 'Authorization': self.api_key }
    if data is not None:
      data = json.dumps(data)
      headers['Content-Type'] = 'application/json'

    if self.debug == True:
      print "HEADERS:"
      for key, value in headers.iteritems():
        print "%s: %s" % (key, value)
      print "DATA:"
      print data
      print "URL:"
      print url

    try:
      req = urllib2.Request(url=url, headers=headers, data=data)
      f = urllib2.urlopen(req)
      return json.loads(f.read())
    except Exception, e:
      return {
      "code":e.code,
      "reason":e.reason
      }