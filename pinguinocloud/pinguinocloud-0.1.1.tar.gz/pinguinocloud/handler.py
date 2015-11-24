#!/usr/bin/env python


import sys
import os

import requests

from . import info
from .core.pinguino import Pinguino
from .core.boards import boardlist
from .login import Login


# Python3 compatibility
if os.getenv("PINGUINO_PYTHON") is "3":
    #Python3
    from tkinter import Tk
    from configparser import RawConfigParser
else:
    #Python2
    from Tkinter import Tk
    from configparser import RawConfigParser



########################################################################
class PinguinoHandler(object):
    """"""

    #HOST = "http://localhost:8888/handler"

    URL_LOGIN = "http://localhost:8000/core/handler/login"
    URL_HASH = "http://localhost:8000/core/handler/user_hash"

    URL_REPORT = "http://pinguinocloud.herokuapp.com"


    #----------------------------------------------------------------------
    def __init__(self):

        self.client = requests.session()

        # self.enable_logs()
        self.username, self.password = self.get_auth()
        self.login_app()

        URI = sys.argv[1]
        operation, args = URI.split("?")
        self.generate_attr(args)

        if operation == "info":
            self.send_info()

        else:  #hex data
            self.upload(operation)


    #----------------------------------------------------------------------
    def send_info(self):

        mydata["type"] = "info"
        self.generate_report(mydata)


    #----------------------------------------------------------------------
    def upload(self, hex_):

        hex_file = self.generate_temp_hex(hex_)

        pdev = Pinguino()
        board = self.get_board()
        pdev.set_board(board)
        # boot = pdev.dict_boot[self.boot]
        # pdev.set_bootloader(*boot)

        pdev.__hex_file__ = hex_file

        uploaded, data = pdev.upload()

        if uploaded:
            mydata = {"uploaded": "true",}
        else:
            mydata = {"uploaded": "false",
                      "message": data,
                      }

        mydata["type"] = "modal"
        self.generate_report(mydata)


    #----------------------------------------------------------------------
    def login_app(self):

        #LOGIN_URL = self.HOST + self.URL_LOGIN
        self.client.get(self.URL_LOGIN)

        csrftoken = self.client.cookies['csrftoken']

        data = {"username": self.username,
                "password": self.password,
                "csrfmiddlewaretoken": csrftoken,
                }

        login = self.client.post(self.URL_LOGIN, data=data)

        if not login.json()["login"]:
            self.username, self.password = self.show_loggin(auth_file = os.path.join(self.get_user_dir(), "auth"))
            self.login_app()



    #----------------------------------------------------------------------
    def generate_report(self, mydata):

        req = self.client.get(self.URL_HASH)
        mydata["user"] = req.json()["hash"]

        self.client.get(self.URL_REPORT, data=mydata)


    #----------------------------------------------------------------------
    def get_board(self):

        for board in boardlist:
            if board.board == self.board: break
        return board


    #----------------------------------------------------------------------
    def generate_attr(self, args):

        print("Attrs")
        print("-" * 70)
        for element in args.split("&"):
            name, value = element.split("=")
            setattr(self, name, value)
            print("{}: {}".format(name, value))
        print("-" * 70)


    #----------------------------------------------------------------------
    def generate_temp_hex(self, hex_):

        hex_ = hex_.replace("#", ":")
        hex_ = hex_.replace("pinguino://", "")
        hex_ = hex_.replace(":", "\n:")
        hex_ = hex_[1:] + "\n"

        hex_file = os.path.join(self.get_user_dir(), "temp.hex")
        if os.path.isfile(hex_file): os.remove(hex_file)
        with open(hex_file, "w") as temp_file: temp_file.write(hex_)

        return hex_file


    #----------------------------------------------------------------------
    def get_user_dir(self):

        user_dir = os.path.expanduser("~/.pinguino/cloud")
        if not os.path.isdir(user_dir):
            os.mkdir(user_dir)

        return user_dir



    #----------------------------------------------------------------------
    def enable_logs(self):

        debug_file = os.path.join(self.get_user_dir(), "log")
        debug = open(debug_file, "w")
        sys.stdout = debug
        sys.stderr = debug



    #----------------------------------------------------------------------
    def get_auth(self):

        auth_file = os.path.join(self.get_user_dir(), "auth")
        if not os.path.isfile(auth_file):
            return self.show_loggin(auth_file)

        else:

            auth = RawConfigParser()
            auth.readfp(open(auth_file))

            if auth.has_option("Auth", "username") and auth.has_option("Auth", "password"):
                return auth.get("Auth", "username"), auth.get("Auth", "password")
            else:
                return self.show_loggin(auth_file)



    #----------------------------------------------------------------------
    def show_loggin(self, auth_file):

        root = Tk()
        app = Login(master=root, auth_file=auth_file)
        app.mainloop()
        return app.username_, app.password_




if __name__ == "__main__":
    PinguinoHandler()
