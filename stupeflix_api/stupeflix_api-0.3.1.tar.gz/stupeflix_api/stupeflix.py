"""
Stupeflix web services python client : stupeflix.py

This is the main entry point for using stupeflix video generation web service.

See README for more information

http://www.stupeflix.com
http://code.google.com/p/stupeflix/

Copyright (c) 2008 Francois Lagunas, http://www.stupeflix.com

"""

import urllib
from stupeflixbase import StupeflixBase
import demjson
import xml.sax.saxutils as saxutils
import connection
import types

# TODO : file streaming

class StupeflixClient(StupeflixBase): 
    def __init__(self, accessKey, privateKey, host = "http://services.stupeflix.com", service = 'stupeflix-1.0', debug = False):
        if host.endswith("/"):
            host = host[:-1]
        super(StupeflixClient, self).__init__(accessKey, privateKey, host, service, debug)
        self.batch = False
        self.batchData = ""

    # Start a batch, used for speeduping video definition upload
    # Operation that can be batched : sendDefinition and createProfiles
    # Operation 
    # Only works for xml definition, not zip, and xml must be in UTF8
    def batchStart(self, maxSize = 1000000):
        self.batch = True
        self.batchData = "<batch>"
        self.batchMaxSize = maxSize

    # End a batch: actually send data
    def batchEnd(self):
        self.batchData += "</batch>"
        self.sendDefinitionBatch(body = self.batchData)
        self.batchData = ""
        self.batch = False

    # Send a definition file to the API
    def sendDefinition(self, user, resource, filename = None, body = None):
        url = self.definitionUrl(user, resource)
        if body:
            contentType = self.TEXT_XML_CONTENT_TYPE;
        elif self.isZip(filename):
            contentType = self.APPLICATION_ZIP_CONTENT_TYPE
        else:
            contentType = self.TEXT_XML_CONTENT_TYPE
        if self.batch and contentType == self.TEXT_XML_CONTENT_TYPE:
            self.batchData += "<task user=\"%s\" resource=\"%s\">" % (user, resource)
            if body:                
                self.batchData += body
            else:
                self.batchData += open(filename, 'rb').read()
        else:
            return self.sendContent("PUT", url, contentType, filename, body)

    # Send a definition file to the API
    def sendDefinitionBatch(self, filename = None, body = None):
        url = self.definitionBatchUrl()
        contentType = self.TEXT_XML_CONTENT_TYPE;
        return self.sendContent("PUT", url, contentType, filename, body)

    def getDefinition(self, user, resource, filename):
        url = self.definitionUrl(user, resource)
        return self.getContent(url, filename)['size']
    
    def _getAbsoluteUrl(self, url, followRedirect = False):
        urlPart = self.getContentUrl(url, 'GET', None)
        if followRedirect:
            conn = connection.Connection(self.base_url, followRedirect = False)
            response = conn.request_get(urlPart)
            if "location" in response["headers"]:
                return response["headers"]["location"]
            else:
                return self.base_url + urlPart
        else:
            return self.base_url + urlPart
      
    def getDefinitionUrl(self, user, resource):
        url = self.definitionUrl(user, resource)
        return self._getAbsoluteUrl(url)
      
    def getProfileUrl(self, user, resource, profile, followRedirect = False):
        url = self.profileUrl(user, resource, profile)
        return self._getAbsoluteUrl(url, followRedirect)

    def getProfile(self, user, resource, profile, filename):
        url = self.profileUrl(user, resource, profile)
        return self.getContent(url, filename)['size']

    def getProfileThumbUrl(self, user, resource, profile, followRedirect = False):
        url = self.profileThumbUrl(user, resource, profile, "thumb.jpg")
        return self._getAbsoluteUrl(url, followRedirect)

    def getProfileThumb(self, user, resource, profile, filename):
        url = self.profileThumbUrl(user, resource, profile, "thumb.jpg")
        return self.getContent(url, filename)['size']

    def getProfileReportUrl(self, user, resource, profile, followRedirect = False):
        url = self.profileReportUrl(user, resource, profile)
        return self._getAbsoluteUrl(url, followRedirect)

    def getProfileReport(self, user, resource, profile, filename):
        url = self.profileReportUrl(user, resource, profile)
        return self.getContent(url, filename)['size']

    def getProfilePreviewUrl(self, user, resource, profile):
        url = self.profilePreviewUrl(user, resource, profile)
        return self._getAbsoluteUrl(url, False)
    
    def createProfiles(self, user, resource, profiles):
        profileData = ""
        if isinstance(profiles, list):
            profileData = "<profiles>"
            for p in profiles:
                profileData += "<profile name=\"%s\"><stupeflixStore/></profile>" % p
            profileData += "</profiles>"
        elif isinstance(profiles, StupeflixProfileSet):
            profileData = profiles.xmlGet()
        else:
            profileData = profiles
        if self.batch:
            self.batchData += profileData
            self.batchData += "</task>"
            if len(self.batchData) >= self.batchMaxSize:        
                try:
                    self.batchEnd()
                finally:                    
                    self.batchStart(self.batchMaxSize)
        else:
            url, parameters = self.profileCreateUrl(user, resource, profileData)
            contentType = self.APPLICATION_URLENCODED_CONTENT_TYPE
            body = urllib.urlencode(parameters)

            return self.sendContent("POST", url, contentType, body = body)

    def cancelProfiles(self, user, resource, profiles):
        url, parameters = self.profileCancelUrl(user, resource, profileData)
        contentType = self.APPLICATION_URLENCODED_CONTENT_TYPE
        body = urllib.urlencode(parameters)

        return self.sendContent("DELETE", url, contentType, body = body)

    def getStatus(self, user = None, resource = None, profile = None, marker = None, maxKeys = None):
        url, parameters = self.statusUrl(user, resource, profile, marker, maxKeys)
        ret = self.getContent(url, parameters = parameters)
        status = demjson.decode(ret['body'], encoding='utf-8' )    
        return status

    def getMarker(self, status):
        if len(status) == 0:
            return None
        lastStatus = status[-1]
        return map(lambda x: lastStatus[x], ["user", "resource", "profile"])

    # helper functions : build non signed urls for each kind of action
    def definitionUrl(self, user, resource):
        return "/%s/%s/definition/" % (user, resource)

    # helper functions : build non signed urls for each kind of action
    def definitionBatchUrl(self):
        return "/batch/"

    def profileUrl(self, user, resource, profile):
        return "/%s/%s/%s/" % (user, resource, profile)

    def profileThumbUrl(self, user, resource, profile, thumbname):
        return "/%s/%s/%s/%s/" % (user, resource, profile, thumbname)

    def profileReportUrl(self, user, resource, profile):
        return "/%s/%s/%s/%s/" % (user, resource, profile, "report.xml")

    def profilePreviewUrl(self, user, resource, profile):
        return "/%s/%s/%s/%s/" % (user, resource, profile, "preview.flv")

    def profileCreateUrl(self, user, resource, profiles):
        s = "/%s/%s/" % (user, resource)
        parameters = {self.XML_PARAMETER:profiles.encode("utf8")}
        return s, parameters
    
    def actionUrl(self, user, resource, profile, action):
        path = [user, resource, profile]
        s = ""
        for p in path:
            if p == None:
                break
            s += "/%s" % p
        s += "/%s/" % action            
        return s

    def statusUrl(self, user, resource, profile, marker = None, maxKeys = None):
        params = {}
        if marker != None:
            params[self.MARKER_PARAMETER] = "/".join(marker)
        if maxKeys != None:
            params[self.MAXKEYS_PARAMETER] = maxKeys

        return self.actionUrl(user, resource, profile, "status"), params

class StupeflixXMLNode(object):
    def __init__(self, nodeName, attributes = None, children = None, text = None):
        self.children = children
        self.attributes = attributes
        self.nodeName = nodeName
        self.text = text

    def xmlGet(self):
        docXML = '<' + self.nodeName 
        if self.attributes and len(self.attributes) != 0:
            for k,v in self.attributes.iteritems():
                docXML += " "
                if v == None:
                    v = ""
                k = str(k)
                v = str(v)
                docXML += k + '=' + saxutils.quoteattr(v)
        docXML += '>'
        if self.children:
            for c in self.children:
                docXML += c.xmlGet()
        if self.text:
            docXML += saxutils.escape(self.text)
        docXML += '</' + self.nodeName + '>'
        
        return docXML

    def metaChildrenAppend(self, meta = None, notify = None, children = None):
        childrenArray = []
        if meta:
            childrenArray += [meta]
        if notify:
            childrenArray += [notify]
        if children:
            childrenArray += children
        return childrenArray

class StupeflixMeta(StupeflixXMLNode):
    def __init__(self, dict):
        children = []
        for k,v in dict.iteritems():
            children += [StupeflixXMLNode(k, None, None, v)]
        super(StupeflixMeta, self).__init__("meta", {}, children)

class StupeflixProfileSet(StupeflixXMLNode):
    def __init__(self, profiles, meta = None, notify = None):
        children = self.metaChildrenAppend(meta, notify, profiles)
        super(StupeflixProfileSet, self).__init__("profiles", {}, children)

    @staticmethod
    def deflt(profiles):
        profSet = []
        for p in profiles:
            upload = StupeflixDefaultUpload()
            profSet += [StupeflixProfile(p, [upload])]
            
        return StupeflixProfileSet(profSet)

class StupeflixProfile(StupeflixXMLNode):
    def __init__(self, profileName, uploads = None, meta = None, notify = None):
        children = self.metaChildrenAppend(meta, notify, uploads)
        super(StupeflixProfile, self).__init__("profile", {"name":profileName}, children)
        
class StupeflixNotify(StupeflixXMLNode):
    def __init__(self, url, statusRegexp):
        super(StupeflixNotify, self).__init__("notify", {"url":url, "statusRegexp":statusRegexp})

class StupeflixHttpHeader(StupeflixXMLNode):
    def __init__(self, key, value):
        super(StupeflixHttpHeader, self).__init__("header", {"key":key, "value":value})
            
class StupeflixUpload(StupeflixXMLNode):
    def __init__(self, name, parameters, meta = None, notify = None, children = None):
        children = self.metaChildrenAppend(meta, notify, children)
        super(StupeflixUpload, self).__init__(name, parameters, children)           
        
class StupeflixHttpPOSTUpload(StupeflixUpload):
    def __init__(self, url, meta = None, notify = None):
        super(StupeflixHttpPOSTUpload, self).__init__("httpPOST", {"url":url}, meta, notify)

class StupeflixHttpPUTUpload(StupeflixUpload):
    def __init__(self, url, meta = None, notify = None, headers = None):
        super(StupeflixHttpPUTUpload, self).__init__("httpPUT", {"url":url}, meta, notify, headers)
        
class StupeflixYoutubeUpload(StupeflixUpload):
    def __init__(self, login, password, meta = None, notify = None):
        super(StupeflixYoutubeUpload, self).__init__("youtube", {"login":login, "password":password}, meta, notify)

class StupeflixYoutubeTokenUpload(StupeflixUpload):
    def __init__(self, developerKey, token, meta = None, notify = None):
        super(StupeflixYoutubeTokenUpload, self).__init__("youtube", {"developerkey":developerKey, "sid":token}, meta, notify)

class StupeflixYoutubeOAuthUpload(StupeflixUpload):
    def __init__(self, developerKey, oauthconsumerkey, oauthconsumersecret, oauthtoken, oauthtokensecret, meta = None, notify = None):
        super(StupeflixYoutubeOAuthUpload, self).__init__("youtube", 
                                                          {"developerkey":developerKey,
                                                           "oauthconsumerkey" : oauthconsumerkey, 
                                                           "oauthconsumersecret": oauthconsumersecret, 
                                                           "oauthtoken" : oauthtoken, 
                                                           "oauthtokensecret" : oauthtokensecret},
                                                          meta, notify)

class StupeflixBrightcoveUpload(StupeflixUpload):
    def __init__(self, token, reference_id = None, meta = None, notify = None):
        parameters = {"sid":token}
        if reference_id != None:
            parameters["reference_id"] = reference_id
        super(StupeflixBrightcoveUpload, self).__init__("brightcove", parameters, meta, notify)

class StupeflixFacebookTokenUpload(StupeflixUpload):
    def __init__(self, apiKey, secret, token, meta = None, notify = None):
        super(StupeflixFacebookTokenUpload, self).__init__("facebook", {"apikey":apiKey, "secret":secret, "sid":token}, meta, notify)

class StupeflixDailymotionUpload(StupeflixUpload):
    def __init__(self, login, password, sid = None, meta = None, notify = None):
        if not isinstance(sid, (str, unicode, types.NoneType)) or not isinstance(login, (str, unicode, types.NoneType)) or not isinstance(password, (str, unicode, types.NoneType)):
            raise Exception("Bad type for sid = '%s'" % sid)
        if sid != None:
            parameters = {"sid":sid}
        else:
            parameters = {"login":login, "password":password}
        super(StupeflixDailymotionUpload, self).__init__("dailymotion", parameters, meta, notify)

class StupeflixDefaultUpload(StupeflixUpload):
    def __init__(self, meta = None, notify = None):
        children = self.metaChildrenAppend(meta)
        super(StupeflixDefaultUpload, self).__init__("stupeflixStore", {}, meta, notify)

class StupeflixFTPUpload(StupeflixUpload):
    def __init__(self, server, login, password, directory, meta = None, notify = None):
        if not isinstance(server, (str, unicode, types.NoneType)):
            raise Exception("Bad type for server")

        if not isinstance(login, (str, unicode, types.NoneType)):
            raise Exception("Bad type for login")

        if not isinstance(password, (str, unicode, types.NoneType)):
            raise Exception("Bad type for password")

        if not isinstance(directory, (str, unicode, types.NoneType)):
            raise Exception("Bad type for directory")

        parameters = {"login":login, "password":password, "directory":directory, "server":server}
        super(StupeflixFTPUpload, self).__init__("ftp", parameters, meta, notify)
        
class StupeflixS3Upload(StupeflixUpload):
    def __init__(self, bucket, resourcePrefix, accesskey = None, secretkey = None, meta = None, notify = None):
        parameters = {"bucket":bucket, "resourcePrefix":resourcePrefix}
        if accesskey != None: 
            parameters["accesskey"] = accesskey
        if secretkey != None:
            parameters["secretkey"] = secretkey
        super(StupeflixS3Upload, self).__init__("s3", parameters, meta, notify) 
