# Copyright 2010 Blade Network Technologies

import os, sys, warnings
warnings.simplefilter("ignore", DeprecationWarning)


class edit_config (object):
    def __init__(self, opts={}):
        self._dOptions = {
            'target':['-t', '--target', 'TARGET', 'Target datastore'],
            'cfgtxf':['-f', '--cfgtxf', 'CFGTXF', 'Config text file'],
            'defopr':['-d', '--defopr', 'DEFOPR', 'Default operation'],
            'erropt':['-r', '--erropt', 'ERROPT', 'Error option'],
            }
        opts.update(self._dOptions)

    def getopts(self):
        return self._dOptions

    # input missing operation parameters
    def fill(self, params={}):
        if params.has_key('target') == False or params['target'] == '':
            params.update({'target':raw_input('Enter Target datastore: ')})

        if params.has_key('defopr') == False or params['defopr'] == '':
            params.update({'defopr':'merge'})

        if params.has_key('erropt') == False or params['erropt'] == '':
            params.update({'erropt':'stop-on-error'})

        if params.has_key('cfgtxt') == True and params['cfgtxt'] != '':
            pass
        elif params.has_key('cfgtxf') == True and params['cfgtxf'] != '':
            pass
        else:
            params.update({'cfgtxf':raw_input('Enter Config text file: ')})

    def readmsg(self, params={'messageid':100}):
        cfgtxt = ''
        try:
            filename = params['cfgtxf']
            f = open(filename, 'r')
            for line in f.readlines():
                cfgtxt += line
            f.close
        except:
            cfgtxt = ''

        msg = "\
<rpc message-id='%d'>\n\
  <edit-config>\n\
    <target><%s/></target>\n\
    <default-operation>%s</default-operation>\n\
    <error-option>%s</error-option>\n\
    <config-text>\n\
      <configuration-text>\n\
      %s\n\
      </configuration-text>\n\
    </config-text>\n\
  </edit-config>\n\
</rpc>\n" % (params['messageid'], params['target'], params['defopr'], params['erropt'], cfgtxt)

        return msg

    def parsemsg(self, params={'recvmsg':''}):
        if '<ok' not in params['recvmsg']:
            print 'RPC <edit-config> failed:'
            print params['recvmsg']
        params.update({'writemsg':''})

    def writemsg(self, params={'writemsg':''}):
        pass


