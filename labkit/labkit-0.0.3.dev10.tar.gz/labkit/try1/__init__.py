#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


class A(dict):


    def __init__(self):
        self.x=1
        self.y=1

    def new(self):
        print "A"
class B(A):
    def __init__(self):
        super(B,self).__init__()


    def new(self):
        print "haha"

class C(dict):
    def to_dict(self):
        return self.__dict__

a=A()
b=B()
c=C()
print a.__dict__
print b.__dict__
print c.__dict__

a.z={"hello":"world"}

c.__dict__=a.__dict__

b.__dict__={"z":1}

print c.z
a.z="hh"

print c.z
k=c.to_dict()

print k


k.update({"hello":"world"})
print c.__dict__
# c和k字典共享
print c.hello




exit(0)




import  json
print json.dumps(a.__dict__)

b.append(1)
a.append(1)

print json.dumps(b)

c=B()

c.new()
print c.__dict__
