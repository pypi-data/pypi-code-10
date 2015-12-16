
import requests 

from .conversation import Conversation

class Inbox(object):
    
    def __init__(self, inbox):
        """
        Initializes inbox 

            :param api - object of GraphAPI class 
            :param inbox - dictionary which can be got from GraphAPI.get("/me/inbox")
        """
        self.data = inbox 

    def next(self): 
        """
        Returns Inbox object as next page. Facebook does not provide whole inbox at once and uses paging. 
        """
        return Inbox(requests.get(self.data["paging"]["next"]).json())

    def prev(self): 
        """
        Returns Inbox object as previous page. Facebook does not provide whole inbox at once and uses paging. 
        """
        return Inbox(requests.get(self.data["paging"]["prev"]).json())
    
    def has_next(self):
        return "paging" in self.data and "next" in self.data["paging"]

    def has_prev(self):
        return "paging" in self.data and "previous" in self.data["paging"]

    def get_conversations(self):
        """
        Returns list of Conversation objects 
        """
        cs = self.data["data"]
        res = []
        for c in cs:
            res.append(Conversation(c))
        return res


