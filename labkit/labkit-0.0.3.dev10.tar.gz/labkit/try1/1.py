#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


class A():
    a=1
    def set_a(self,a):
        A.a=a
        return self


    @staticmethod
    def new():
        print "new"

    def halt(self):
        # good()
        print A.a
        print outside
        A.new()

outside="outside"


A().set_a(2).halt()

# A().halt()


if __name__ == '__main__':
    pass


