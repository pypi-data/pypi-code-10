#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python

'''accept 1 argument for pid then retuen the pid tree of it'''

import os
import sys
root=sys.argv[1]
import string
ps_message=os.popen('ps lx').readlines()
ps_message=map(string.strip,ps_message)
pid=[]
ppid=[]
ps_message.pop(0)
for i in ps_message:
	j=i.split()	
	pid.append(j[2])
	ppid.append(j[3])

def idtree(father):
	ans=[]

	for i in xrange(pid.__len__()):
		if ppid[i]==father:
			ans.extend(idtree(pid[i]))
	ans.append(father)
	return ans

s=idtree(root)

print ' '.join(s)
