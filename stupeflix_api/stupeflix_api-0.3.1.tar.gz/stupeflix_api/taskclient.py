try:
    import simplejson as json
except Exception, e:
    import json
import urllib


class HTTPError(Exception):
    def __init__(self, code, message):
        super(HTTPError, self).__init__("HTTPError %s: %s" % (code, message))


class LizardClient(object):
    def __init__(self,  baseurl, accesskey = None, secret = None, auth_model = "secret"):
        self.auth_model = auth_model
        self.accesskey = accesskey 
        self.secret = secret
        self.token = None
        self.baseurl = baseurl
        self.session = None

        if auth_model == "secret":
            if self.secret == None:
                raise Exception, "Secret key was not specified."
            if not self.baseurl.startswith("https://"):
                raise Exception, "Secret based auth can only be used with https"
        
    def streamingGet(self, url, body):
        line = ""
        opened = urllib.urlopen(url, body)
        while True:           
            c = opened.read(1)
            if c != "\n" and len(c) != 0:
                line += c
                continue                                       
            yield line
            line = ""
            if len(c) == 0:
                break

    def streamingJSONGet(self, url, body = None):
        for line in self.streamingGet(url, body):
            try:
                payload = json.loads(line)
            except ValueError, e:
                raise ValueError, "Could not decode json from line %s" % line
            yield payload    

    def taskPrepare_(self, response = "status", **kwargs):
        parameters = {}
        
        for k,v in kwargs.items():
            if v == None:
                continue
            if isinstance(v, str) or isinstance(v, unicode):
                parameters[k] = v.encode("utf8")
            elif isinstance(v, float) or isinstance(v, int):
                parameters[k] = str(v)
            else:
                parameters[k] = json.dumps(v)

        parameters["response"] = response
        return parameters
            
    def authAdd(self, parameters, auth_model = None):
        if auth_model == None:
            auth_model = self.auth_model
        if auth_model == "secret":
            parameters["secret"] = self.secret
        elif auth_model == "public":
            parameters["accesskey"] = self.accesskey

    def taskDoURL(self, taskType = None, taskkey = None, filekey = None, response = "result", method = "GET", auth_model = None, https = True, **kwargs):
        assert(taskType != None or taskkey != None)
        key0 = taskType if taskType != None else taskkey
        if filekey == None:            
            url = "%s/%s/" % (self.baseurl, key0)
        else:
            url = "%s/%s/%s" % (self.baseurl, key0, filekey)
        parameters = self.taskPrepare_(response = response, **kwargs)

        self.authAdd(parameters, auth_model = auth_model)

        if not https:
            if url.startswith("https://"):
                url = "http" + url[5:]
        else:
            if url.startswith("http://"):
                url = "https" + url[4:]                                

        parameters = urllib.urlencode(parameters)
        if method == "GET":
            return url + "?" + parameters, None
        elif method == "POST":
            return  url, parameters
        else:
            raise Exception, "Invalid method"

    # Return meta, content
    def taskDo(self, taskType = None, taskkey = None, filekey = None,  response = "result", method = "GET", **kwargs):
        url, body = self.taskDoURL(taskType = taskType, taskkey = taskkey, filekey = filekey, response = response, method = method, **kwargs)
#        print url, body
        if response in ["result"]:
            return urllib.urlopen(url, body)
        elif response in ["status", "status_final"]:
            # Return single object
            u = urllib.urlopen(url, body)            
            body = u.read()
            code = 200
            try:
                code = u.getcode()
            except Exception, e:
                pass
            if code >= 400 and code < 600:
                raise HTTPError(code, body)
            try:
                ret = json.loads(body)
                return ret
            except Exception, e:
                raise Exception, "Could not decode json from %s" % body
        elif response in ["status_stream"]:
            # Return generator suitable for "for x in " loop
            return self.streamingJSONGet(url, body)
        else:
            raise Exception, "Invalid response type %s, should be in result, status, status_final, status_streaming" % response
