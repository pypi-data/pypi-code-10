# Copyright 2010 Blade Network Technologies

import os, sys, warnings
warnings.simplefilter("ignore", DeprecationWarning)


class get_configuration (object):
    def __init__(self, opts={}):
        self._dOptions = {
            'cfgtxf':['-f', '--cfgtxf', 'CFGTXF', 'Output Config text file'],
            }
        opts.update(self._dOptions)

    def getopts(self):
        return self._dOptions

    def fill(self, params={}):
        return

    def readmsg(self, params={'messageid':100}):
        msg = "\
<rpc message-id='%d'>\n\
  <get-configuration database=\"committed\" format=\"text\"/>\n\
</rpc>\n" % params['messageid']
        return msg

    def parsemsg(self, params={'recvmsg':''}):
        if '<rpc-error' in params['recvmsg']:
            print 'RPC <get-configuration> failed:'
            print params['recvmsg']
            params.update({'writemsg':''})
        else:
            # parser configuration text
            cfgtxt_s = '<configuration-text'
            cfgtxt_e = '</configuration-text>'
            try:
                cfgtxt = params['recvmsg']
                idx = cfgtxt.index(cfgtxt_s)
                cfgtxt = cfgtxt[idx:]
                idx = cfgtxt.index('>')
                cfgtxt = cfgtxt[idx+1:]
                idx = cfgtxt.index(cfgtxt_e)
                cfgtxt = cfgtxt[:idx]
            except:
                cfgtxt = ''
            params.update({'writemsg':cfgtxt})

    def writemsg(self, params={'writemsg':''}):
        try:
            if len(params['writemsg']) > 0:
	            filename = params['cfgtxf']
	            f = open(filename, 'w+')
	            f.write(params['writemsg'])
	            f.close
        except:
            print 'RPC <get-configuration>: Configuration:'
            print params['writemsg'] if params.has_key('writemsg') else ''


