# Copyright 2010 Blade Network Technologies

import os, sys, warnings
warnings.simplefilter("ignore", DeprecationWarning)


class get_interface_information (object):
    def __init__(self, opts={}):
        self._dOptions = {
            'portnum':['-n', '--portnum', 'PORTNUM', 'Interface port number'],
            'ipindex':['-i', '--ipindex', 'IPINDEX', 'Interface ip index'],
            'ifinfof':['-f', '--ifinfof', 'IFINFOF', 'Output Interface information file'],
            'brief':['-b', '--brief', '', 'Show brief information'],
            }
        opts.update(self._dOptions)

    def getopts(self):
        return self._dOptions

    def fill(self, params={}):
        return

    def readmsg(self, params={'messageid':100}):
        msg = "\
<rpc message-id='%d'>\n\
  <get-interface-information>\n" % params['messageid']

        if params.has_key('portnum') == True and params['portnum'] != '':
            msg += "    <interface-name> port %s </interface-name>\n" % params['portnum']
        if params.has_key('ipindex') == True and params['ipindex'] != '':
            msg += "    <interface-name> ip %s </interface-name>\n" % params['ipindex']

        if params.has_key('brief') == True and params['brief'] == True:
            msg += "    <brief/>\n"
        else:
            msg += "    <detail/>\n"

        msg += "\
  </get-interface-information>\n\
</rpc>\n"
        return msg

    def parsemsg(self, params={'recvmsg':''}):
        if '<rpc-error' in params['recvmsg']:
            print 'RPC <get-interface-information> failed:'
            print params['recvmsg']
            params.update({'writemsg':''})
        else:
            # parser interface-information
            cfgtxt_s = '<interface-information'
            cfgtxt_e = '</interface-information>'
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
	            filename = params['ifacinf']
	            f = open(filename, 'w+')
	            f.write(params['writemsg'])
	            f.close
        except:
            print 'RPC <get-interface-information>: Information:'
            print params['writemsg'] if params.has_key('writemsg') else ''


