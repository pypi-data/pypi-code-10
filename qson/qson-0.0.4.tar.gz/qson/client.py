import json
import urllib2

import server

HOST = "localhost"

class client(object):
    def __init__(self, host=HOST, port=server.PORT, protocol="http"):
        super(client, self).__init__()
        self.host = host
        self.port = port
        self.protocol = protocol

    def post(self, data):
        url = "{0}://{1}:{2}/".format(self.protocol, self.host, self.port)
        req = urllib2.Request(url, data, {"Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        return response

    def send(self, data):
        if "key" in data:
            key = data["key"]
        else:
            key = False
        data = json.dumps(data)
        response = self.post(data)
        try:
            response = json.load(response)
        except Exception as error:
            print error
            response = {
                "key": key,
                "value": None,
            }
        return response

    def set(self, key, value):
        data = {
            "key": key,
            "value": value,
        }
        response = self.send(data)
        return response["value"]

    def get(self, key):
        data = {
            "key": key,
        }
        response = self.send(data)
        return response["value"]

    def dump(self):
        data = {
            "dump": True,
        }
        response = self.send(data)
        return response

    def load(self, loadData):
        data = {
            "load": loadData,
        }
        response = self.send(data)
        return response["key"]

    def saveFile(self, filePath):
        response = self.dump()
        fileHandle = open(filePath, 'wb')
        json.dump(response, fileHandle)
        fileHandle.close()
        return response

    def loadFile(self, filePath):
        fileHandle = open(filePath, 'rb')
        data = {
            "load": json.load(fileHandle),
        }
        fileHandle.close()
        response = self.send(data)
        return response["key"]

    def __call__(self, key, value=False):
        if value:
            return self.set(key, value)
        return self.get(key)
