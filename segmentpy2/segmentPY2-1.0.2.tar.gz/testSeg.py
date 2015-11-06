# -*- coding: utf8 -*-
import segmentPY2 as segmentPY 
import sys
from oedipus.setting.setting_main import *
def testSegment(words):
    result=segmentPY.getBasic(words)
    result1=segmentPY.getSplit(words)
    result2=segmentPY.getPhrase(words)
    result3=segmentPY.getBasicPhrase(words)
    print  'Basic:',result.decode('gbk') 
    print  'Split:',result1.decode('gbk') 
    print 'Phrase:', result2.decode('gbk')
    print 'BasicPhrase:', result3.decode('gbk') 
segmentPY.init(DICT_PATH)
key = u'呷哺呷哺'
key = u'北京百脑汇'
#key = raw_input('input:')
#print key
key = u'商业街'
key = u'林北路 7天'
key = u'北京闫三毛骨病中医院'
key = u'中医骨病'
key = key.encode('gbk')
testSegment(key)
#f=open('test.txt')
#line=f.readline()
#num=0
#while line!='':
#    line=line.strip()
#    line=line.decode('utf-8')
#    line=line.encode('gbk')
#    if len(line)<2:
#        print 'too short'
#        continue
#    print segmentPY.getBasic(line)
#    testSegment(line)
#    line=f.readline()
#
exit
