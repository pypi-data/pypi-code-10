"""
stupeflixbase.py

Base code for the Stupeflix video generation web services.
See stupeflix.py and LICENSE.txt for more information.

http://www.stupeflix.com
http://code.google.com/p/stupeflix/

"""

import os
import hashlib
import base64 
import connection
import time
import hmac
import logging


logger = logging.getLogger(__name__)


class StupeflixBase(object): 
    def __init__(self, accessKey, privateKey, host = "http://services.stupeflix.com", service = 'stupeflix-1.0', debug = False):
        self.accessKey = str(accessKey)
        self.privateKey = str(privateKey)
        self.base_url = host + '/' + service
        self.debug = debug
        self.service = service
        self.TEXT_XML_CONTENT_TYPE = "text/xml"
        self.APPLICATION_ZIP_CONTENT_TYPE = "application/zip"
        self.APPLICATION_JSON_CONTENT_TYPE = "application/json"
        self.APPLICATION_URLENCODED_CONTENT_TYPE = "application/x-www-form-urlencoded"
        self.PROFILES_PARAMETER = "Profiles"
        self.XML_PARAMETER = "ProfilesXML"
        self.MARKER_PARAMETER = "Marker"
        self.MAXKEYS_PARAMETER = "MaxKeys"
        # Currently there is only the Marker parameter (used for partial enumeration)
        self.parametersToAdd = [self.MARKER_PARAMETER, self.MAXKEYS_PARAMETER]
        # Time between two retry (to wait for Amazon S3)
        self.sleepTime = 5.0
        self.maxRetry = 5
        self.base = True

    def connectionGet(self, base_url = None):
        if base_url == None:
            base_url = self.base_url
        return connection.Connection(base_url)

    def paramString(self, parameters):
        paramStr = ""
        if parameters:
            for p in self.parametersToAdd:
                if p in parameters:
                    paramStr += "%s\n%s\n" % (p, parameters[p])


        if isinstance(paramStr, unicode):
            paramStr = paramStr.encode("utf8")

        return paramStr

    def strToSign(self, method, resource, md5, mime, datestr, parameters):
        paramStr = self.paramString(parameters)
        stringToSign  = "%s\n%s\n%s\n%s\n%s\n%s" % (method, md5, mime, datestr, '/' + self.service + resource, paramStr)
        return stringToSign
        
    def sign(self, strToSign, secretKey):               
        h = hmac.new(secretKey, strToSign, hashlib.sha1)
        sig = h.hexdigest()
        return sig

    def signUrl(self, url, method, md5, mime, parameters = {}, inlineAuth = False):
        now = int(time.time())
        strToSign = self.strToSign(method, url, md5, mime, now, parameters)            
        signature = self.sign(strToSign, self.privateKey)
        if inlineAuth:
            url += "%s/%s/%s/" % (self.accessKey, signature, now)
        else:
            url += "?Date=%s&AccessKey=%s&Signature=%s" % (now, self.accessKey,signature)
        if parameters:
            for k,v in parameters.items():
                url += "&%s=%s" % (k,v)
        return url

    def md5FileOrBody(self, filename, body = None):
        md5 = hashlib.md5()
        if body != None:
            md5.update(body)
        else:
            chunksize=1024
            f = open(filename, 'rb')
        
            while True:
                chunk = f.read(chunksize)
                if not chunk: break
                md5.update(chunk)
            f.close()     

        digest = md5.digest()
        return (digest, md5.hexdigest(), base64.b64encode(digest)) 

    def isZip(self, filename):
        f = open(filename, 'rb')
        header = f.read(4)
        return header == r'PK'+chr(3)+chr(4)

    def logdebug(self, s):
        if self.debug:
            print str(s)

    def error(self, message):
        self.logdebug(message)
        raise Exception, message

    def answer_error(self, answer, message):
        raise Exception, "%s\n%s" % (message, answer['body'])

    # sendcallback is an object with 
    #  - a 'sendCallBack' member function that accept a unique int argument (=number of bytes written so far)
    #  - a 'sendBlockSize' member function with no argument which return the size of block to be sent
    def sendContent(self, method, url, contentType, filename = None, body = None,  parameters = None, sendcallback = None, streamBody = None, base_url = None):
        if streamBody == None:
            # fix default ascii encoding
            if body:
                body = body.encode('utf-8')

            md5, md5hex, md5base64 = self.md5FileOrBody(filename, body)

            if filename:
                size = os.stat(filename).st_size 
            else:
                if isinstance(body, unicode):
                    body = body.encode("utf8")
                size = len(body)
        else:
            md5, md5hex, md5base64 = streamBody.md5Triplet()
            body = streamBody
            size = None

        # SEND DATA
        conn = self.connectionGet(base_url)

        headers = {'Content-MD5':str(md5base64), 
                   'Content-Type':contentType}

        if size != None:
            headers['Content-Length'] = str(size)
        else:
            headers['Transfer-Encoding'] = 'chunked'

        url = self.signUrl(url, method, md5base64, contentType, parameters)

        # LAUNCH THE REQUEST : TODO : pass filename instead of body 
        if method == "PUT":
            answer = conn.request_put(url, filename = filename, body = body, headers = headers, sendcallback = sendcallback)
        elif method == "POST":
            answer = conn.request_post(url, filename = filename, body = body, headers = headers)
        elif method == "DELETE":
            answer = conn.request_delete(url, headers = headers)

        headers = answer['headers']

        self.logdebug(headers)
        self.logdebug(answer['body'])

        # NOW CHECK THAT EVERYTHING IS OK
        status = headers['status']
        if status != '200':
            msg = "sendContent : bad STATUS %s" % status
            self.answer_error(answer, msg)
        
        if 'etag' not in headers:
            msg = "corrupted answer: no etag in headers. Response body is " + answer['body']
            self.error(msg)
            
        obtainedMD5 = headers['etag'].strip('"')         

        if obtainedMD5 != md5hex:
            msg = "sendContent : bad returned etags %s =! %s (ref)" % (obtainedMD5, md5hex)
            self.error(msg)

        return answer

    def getContentUrl(self, url, method, parameters, inlineAuth = False):
        return self.signUrl(url, method, "", "", parameters, inlineAuth  = inlineAuth)

    def getContent(self, url, filename = None, parameters = None):
        sleepTime = self.sleepTime
        for i in range(self.maxRetry):
            raiseExceptionOn404 = (i + 1) == self.maxRetry
            ret = self.getContent_(url, filename, parameters, raiseExceptionOn404)
            if ret["status"] != 404:
                return ret
            elif ret["status"] >= 300 and ret["status"] < 400:
                url = ret["url"]            

            logger.info("RETRYING: %s", i)
            time.sleep(sleepTime)

    def getContent_(self, url, filename = None, parameters = None, raiseExceptionOn404 = True):

        method = "GET"
        url = self.getContentUrl(url, method, parameters)

        # GET DATA
        conn = self.connectionGet()
        answer = conn.request_get(url)
        body = answer['body']

        headers = answer['headers']
        status = int(headers['status'])

        ret = {"status":status}
        if 'content-location' in headers:
            ret['url'] = headers['content-location']

        if 'content-length' in headers:
            obtainedSize = int(headers['content-length'])

        if status == 204:
            # there was no content
            obtainedSize = 0
            if len(body) != 0:
                self.error("204 status with non empty body.")
        elif status == 200:
            pass
        elif status == 404 and not raiseExceptionOn404:            
            return ret
        elif status >= 300 and status < 400:
            return ret
        else:
            msg = "getContent, url=%s%s : bad STATUS %s" % (self.base_url, url, status)
            self.answer_error(answer, msg)

        if len(body) != obtainedSize:
            self.error("Non matching body length and content-length")

        if filename != None:
            f = open(filename, 'wb')
            f.write(body)            
            f.close()

            if status == 204:
                os.unlink(filename)
            else:
                filesize = os.stat(filename).st_size             
                if obtainedSize != filesize:
                    os.unlink(filename)
                    self.error("file size is incorrect : file size = %d, body size = %d" % (filesize, obtainedSize))            
                
        # NOW CHECK EVERYTHING IS OK
        md5, md5hex, md5base64 = self.md5FileOrBody(filename, body)

        if status != 204:
            obtainedMD5 = headers['etag'].strip('"') 
            if obtainedMD5 != md5hex:
                if filename:
                    os.unlink(filename)
                    pass
                self.error("getContent : bad returned etag %s =! %s (ref)" % (md5hex, obtainedMD5))

        if status == 200:
            #self.logdebug("headers = %s" % headers)
            ret = {'size':obtainedSize, 'url':url, 'headers': headers}
            if 'content-location' in headers:
                ret['url'] = headers['content-location']
        else:
            ret = {'size':obtainedSize, 'url':url}
        
        if not filename:
            ret['body'] = body

        ret["status"] = status

        return ret

