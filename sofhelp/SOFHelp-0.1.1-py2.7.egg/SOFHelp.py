import requests
from BeautifulSoup import BeautifulSoup
import re
import os
import urllib


class SOFHelp:
    proxy_dict = {}
    proxy_enabled = False

    def __init__(self):
        self.url="http://stackoverflow.com/search?"

    def set_proxy(self, http=None, https=None):
        if http != None:
            self.proxy_dict["http"]=http

        if https != None:
            self.proxy_dict["https"]=https

        if self.proxy_dict.has_key("http") or self.proxy_dict.has_key("https"):
            self.proxy_enabled=True
        else:
            self.proxy_enabled=False

    def get_help(self, query):
        build_url = {"q":query}
        query = urllib.urlencode(build_url,"utf-8")
        try:
            if self.proxy_enabled:
                req = requests.get(self.url+query, proxies=self.proxy_dict)
            else:
                req = requests.get(self.url+query)
            res = (req.text).encode(encoding="UTF-8")
            self.soup = BeautifulSoup(res)
            self.get_top_five_results()
        except Exception as e:
            print "Exeception info as below:"
            return str(e)

    def get_top_five_results(self):
        try:
            result_titles = self.soup.findAll(attrs={"class":"result-link"})
            answers=[]
            for title in result_titles:
                s = BeautifulSoup(str(title))
                question = s.find('a').text
                answer = s.find('a')['href']
                ans_set = [question,answer]
                answers.append(ans_set)
            for set in answers[:5]:
                print set[0]
                print "http://stackoverflow.com"+set[1]
        except Exception as e:
            print str(e)
