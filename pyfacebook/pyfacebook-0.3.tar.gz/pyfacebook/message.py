from datetime import datetime


class Message(object):
    
    def __init__(self, data, conversation):
        self.data = data
        self.sender = self.data["from"]["name"]
        self.message = self.data.get("message", "")
        self.time = self.data["created_time"]
        self.conversation = conversation

    def get_sender(self):
        """
        Returns string representing sender name
        """
        return self.sender

    def get_message(self):
        return self.message

    def __str__(self):
        return self.get_message()

    def get_time(self):
        return datetime.strptime(self.time, "%Y-%m-%dT%H:%M:%S%z")

    def __eq__(self, msg):
        return self.get_sender() == msg.get_sender() and self.get_time() == msg.get_time() 
