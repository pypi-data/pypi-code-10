#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

## ==========
import general, six
general.use_dev_general()
reload(general)
# use this code for useing the live develop version of general located in /Users/lhr/_action/python/projects/general/
## ===========


from general.monkey_patch import mmp,Patcher,monkey_patch, monkey_patch_group

patcher=Patcher()

class newlist(list):
    pass

@patcher.as_staticmethod
def new():
    print('good')
    # self.append('x')

@patcher.as_method
def new2(self):
    # print('good')
    self.append('x')




a=newlist()

print(a)

patcher.mmp(newlist)
# mmp(newlist,reg)
# monkey_patch_group(newlist,reg.method_list)

# a.new()
a.new2()
print(a)

new2(a)


