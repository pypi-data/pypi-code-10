import time


def delstring(self, mystring, dellist):
    for deletable in dellist:
        mystring = mystring.replace(deletable, "")
    return mystring


def wait(self, seconds):
    time.sleep(seconds)