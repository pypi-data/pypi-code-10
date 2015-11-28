# Copyright 2010 Blade Network Technologies

import os, sys, warnings
warnings.simplefilter("ignore", DeprecationWarning)


class get_config (object):
    def __init__(self, opts={}):
        self._dOptions = {
            'source':['-s', '--source', 'SOURCE', 'Source datastore'],
            'cfgtxf':['-f', '--cfgtxf', 'CFGTXF', 'Output Config text file'],
            }
        opts.update(self._dOptions)

    def getopts(self):
        return self._dOptions

    def fill(self, params={}):
        if params.has_key('source') == False or params['source'] == '':
            params.update({'source':raw_input('Enter Source datastore: ')})

    def readmsg(self, params={'messageid':100}):
        msg = "\
<rpc message-id='%d'>\n\
  <get-config>\n\
    <source><%s/></source>\n\
    <filter type='subtree'>\n\
      <configuration-text/>\n\
    </filter>\n\
  </get-config>\n\
</rpc>\n" % (params['messageid'], params['source'])
        return msg

    def parsemsg(self, params={'recvmsg':''}):
        if '<rpc-error' in params['recvmsg']:
            print 'RPC <get-config> failed:'
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
            print 'RPC <get-config>: Configuration:'
            print params['writemsg'] if params.has_key('writemsg') else ''


