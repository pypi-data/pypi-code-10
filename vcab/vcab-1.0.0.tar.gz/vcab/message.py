import json

class MessageException(Exception):
    pass

class MalformedMessageException(MessageException):
    pass

class Request(object):
    def __init__(self, command_name, params):
        self.command = command_name
        self.params = params

    @staticmethod
    def parse(message):
        try:
            data = json.loads(message)
        except ValueError as e:
            raise MalformedMessageException("Cannot decode json: %s" % e)
        if 'command' not in data:
            raise MalformedMessageException("Missing key: command")
        if 'params' not in data:
            raise MalformedMessageException("Missing key: params")
        return Request(data['command'], data['params'])

class Response(object):
    def __init__(self, result = '', status = 200, command_name = None):
        self.status = status
        self.command = command_name
        self.body = result

    def __str__(self):
        return json.dumps(self.__dict__)
