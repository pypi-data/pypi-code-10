__author__ = 'k-nakamura'
# -*- coding: utf-8 -*-
from naoqi import ALProxy

class textToSpeech:



    def __init__(self, order):
        self.order = order
        self.pepper_ip = "192.168.100.20"
        self.tts = ALProxy("ALTextToSpeech", self.pepper_ip, 9559)

    def sayText(self):
        say = ""
        for i in self.order:
           say += i + unicode("と", "utf-8")
        say = say[:-1].encode('utf-8')
        self.tts.say(say)




