#!/usr/bin/env python

import os

# Python3 compatibility
if os.getenv("PINGUINO_PYTHON") is "3":
    #Python3
    from tkinter import Frame, LEFT, Label, Entry, X, TOP, Button, RIGHT
    from configparser import RawConfigParser
else:
    #Python2
    from Tkinter import Frame, LEFT, Label, Entry, X, TOP, Button, RIGHT
    from configparser import RawConfigParser


########################################################################
class Login(Frame):

    #----------------------------------------------------------------------
    def __init__(self, master=None, auth_file="auth"):
        Frame.__init__(self, master)

        self.parent = master
        self.auth_file = auth_file
        self.parent.title("Login - Pinguino Cloud")

        self.master.configure(padx=10, pady=10)
        width = 14

        frame8l = Frame(self.parent)
        frame_text2 = Frame(frame8l)
        frame_text2.pack(side=LEFT)
        Label(frame_text2, text="Username:", width=width, anchor="w").pack(side=LEFT)
        self.username = Entry(frame8l)
        self.username.pack(side=LEFT, fill=X, expand=True)
        frame8l.pack(fill=X, expand=True, side=TOP)

        frame32l = Frame(self.parent)
        frame_text4 = Frame(frame32l)
        frame_text4.pack(side=LEFT)
        Label(frame_text4, text="Password:", width=width, anchor="w").pack(side=LEFT)
        self.password = Entry(frame32l, show="*")
        self.password.pack(side=LEFT, fill=X, expand=True)
        frame32l.pack(fill=X, expand=True, side=TOP)


        Button(self.master, text="Login...", command=self.login).pack(side=RIGHT)
        self.centerWindow()


    #----------------------------------------------------------------------
    def login(self):

        self.username_ = self.username.get()
        self.password_ = self.password.get()

        auth = RawConfigParser()
        auth.add_section("Auth")
        auth.set("Auth", "username", self.username_)
        auth.set("Auth", "password", self.password_)

        auth.write(open(self.auth_file, "w"))

        self.master.destroy()


    #----------------------------------------------------------------------
    def centerWindow(self):

        w = 300
        h = 100

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry("{}x{}+{}+{}".format(int(w), int(h), int(x), int(y)))


