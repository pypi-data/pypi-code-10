class QueueBase(object):
    def configure(self, mode, endpoint):
        pass

    def close(self):
        pass

    def connect(self):
        pass

    def accept(self):
        pass

    def send(self, data):
        pass

    def recv(self, blocking):
        pass