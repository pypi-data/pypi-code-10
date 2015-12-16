
from .message import Message
from .exceptions import LimitExceededException

import requests 


class Conversation(object):
    
    def __init__(self, data, comments=None):
        """
        Initializes new Conversation object 

            :param data - dictionary data which can be got from inbox data field 
            :param comments - provide separate comments
        """
        self.data = data.copy()
        if comments != None:
            self.data["comments"] = comments.copy()

    def get_persons(self):
        """
        Returns list of strings which represents persons being chated with 
        """
        cs = self.data["to"]["data"]
        res = [] 
        for c in cs:
            res.append(c["name"])
        return res

    def get_messages(self):
        """
        Returns list of Message objects which represents messages being transported.
        """
        cs = self.data["comments"]["data"]
        res = [] 
        for c in cs:
            res.append(Message(c,self))
        return res

    def next(self):
        """
        Returns next paging
        """
        c = Conversation(self.data, requests.get(self.data["comments"]["paging"]["next"]).json())
        if "error" in c.data["comments"] and c.data["comments"]["error"]["code"] == 613:
            raise LimitExceededException()
        return c

    def prev(self):
        """
        Returns previous paging
        """
        c = Conversation(self.data, requests.get(self.data["comments"]["paging"]["previous"]).json())
        if "error" in c.data["comments"] and c.data["comments"]["error"]["code"] == 613:
            raise LimitExceededException()
        return c
    
    def has_next(self):
        return "paging" in self.data["comments"] and "next" in self.data["comments"]["paging"]
    
    def has_prev(self):
        return "paging" in self.data["comments"] and "previous" in self.data["comments"]["paging"]
    
    def __str__(self):
        s = ""
        for p in self.get_persons():
            s += p + ", "
        return s
