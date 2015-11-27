#!/usr/bin/python
from time import sleep
from random import uniform
import sys
import textwrap

"""
 Author: Ashwani Singh
 date: 27-11-2015
"""

class GoodBye:
    letter = {
        "subject": "Good Bye",
        "start": "Hi All,",
        "line1": "Today is my last working day at abc.",
        "para": "I would like to thank you all for the guidance, "
                  "help and support I have received from all of you in the 2.10 years that I have worked for the company."
                  "I feel that I have prospered both personally as well as professionally thanks to your input."
                  "I wish the company and XXXXians all the best for the future, and hope the company continues to prosper.",
        "last_line": "Stay in touch.",
        "social_links": {
            "mobile": "********",
            "email": "example@gmail.com",
            "linked_in": "https://www.linkedin.com",
            "website": "example.com",

        },
        "footer": [
            "Regard,",
            "Ash Singh",
            "Software Engineer",
            "xxxxxx"
        ]

    }

    @staticmethod
    def type_writer_effect():
        sys.stdout.flush()
        sleep(uniform(0, 0.7))  # random sleep from 0 to 0.3 seconds

    @staticmethod
    def print_wrap(content):
        for text in textwrap.wrap(content):
            print(text)
            GoodBye.type_writer_effect()
    @property
    def print_good_bye(self):
        # starting print

        # printing subject
        print("Subject: %s" % self.letter['subject'])
        GoodBye.type_writer_effect()
        print(self.letter['start'])
        GoodBye.type_writer_effect()
        print(self.letter['line1'])
        GoodBye.type_writer_effect()
        GoodBye.print_wrap(self.letter['para'])
        GoodBye.type_writer_effect()
        print(self.letter['last_line'])
        GoodBye.type_writer_effect()

         # printing social links
        for element in self.letter['social_links']:
            print(element+": " + self.letter['social_links'][element])
            GoodBye.type_writer_effect

        print("\n")
         # printing footer
        for element in self.letter['footer']:
            print(element)
            GoodBye.type_writer_effect()

if __name__ == '__main__':
    good_bye = GoodBye()
    good_bye.print_good_bye