#!/usr/bin/env python

# Copyright 2010 Blade Network Technologies

import os, sys, copy

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

import param, conn
from rpc import rpc

bnc_options = {
    # key:        [shout opt, long opt, parameter,  help message]
    'username':   ['-u', '--username',  'USERNAME',  'login username'],
    'password':   ['-p', '--password',  'PASSWORD',  'login password'],
    'operation':  ['-o', '--operation', 'OPERATION', 'rpc operation'],
    'verbose':    ['-v', '--verbose',   '',          'show more information'],
    'help':       ['-h', '--help',      '',          'show help'],
    }

class bnclient(object):
    """
    Blade NETCONF Client.
    Establish netconf session and exchange message!
    """
    def __init__(self, argv=None):
        # fill argv
        if argv is None:
            self._sName = sys.argv[0]
            self._aArgv = copy.deepcopy(sys.argv[1:])
        else:
            self._sName = argv[0]
            self._aArgv = copy.deepcopy(argv[1:])

        # fill options
        self._dOptions = copy.deepcopy(bnc_options)

        # generate parameter class object
        self._cParams = param.bnc_param()
        # parser argv to parameters
        self._cParams.parser(self._aArgv, self._dOptions)
        # check whether show help
        if self._cParams.get('help') == True:
            self.usage()
            sys.exit()
        # input missing parameters
        self._cParams.fill()

    def usage(self):
        bnc_opts = bnc_options.values()
        print 'Usage: %s [options] hostname[:port]' % self._sName
        if len(bnc_opts) > 0:
            print 'Options:'
            for opt in bnc_opts:
                if len(opt) != 0:
                    if opt[2] != '':
                        print '    %s, %-15s = %-15s : %s' % tuple(opt)
                    else:
                        print '    %s, %-15s %-17s : %s' % tuple(opt)
        try:
            tmp = {}
            rpc.operations[self._cParams.get('operation')](tmp)
            opr_opts = tmp.values()
        except:
            opr_opts = []
        if len(opr_opts) > 0:
            print '  Operation <%s> options:' % self._cParams.get('operation')
            for opt in opr_opts:
                if len(opt) != 0:
                    if opt[2] != '':
                        print '    %s, %-15s = %-15s : %s' % tuple(opt)
                    else:
                        print '    %s, %-15s %-17s : %s' % tuple(opt)

    # connect to server
    def connect(self, timeout=60):
        try:
            # generate connection
            self._hConn = conn.bnc_conn(params=self._cParams.get(), timeout=timeout)
            self._hConn.connect()
        except:
            print 'BNClient: Call connect fail'
            sys.exit()


    # send, recv <hello>
    def sendhello(self):
        try:
            # send hello
            cli_hello_msg = "<hello>\n" +\
                            "  <capabilities>\n" +\
                            "    <capability>urn:ietf:params:netconf:base:1.0</capability>\n" +\
                            "  </capabilities>\n" +\
                            "</hello>\n"
            self._cParams.set('cli_hello', cli_hello_msg)
            self._hConn.sendmsg(cli_hello_msg)

            # recv hello
            ser_hello_msg = self._hConn.recvmsg()
            self._cParams.set('ser_hello', ser_hello_msg)
        except:
            print 'BNClient: Call sendhello fail'
            sys.exit()

        """ end of function exchgcaps """


    def sendrpc(self, argv=[]):
        self._aArgv += argv
        _operation = ''
        try:
            self._cParams.parser(self._aArgv, self._dOptions)

            # set rpc operation handler
            while self._cParams.get('operation') not in rpc.operations.keys():
                self._cParams.set('operation', raw_input("Enter RPC Operation:\n%s:" % rpc.operations.keys()))

            _operation = self._cParams.get('operation')
            self._hRpcOper = rpc.operations[_operation](opts=self._dOptions)
            # input missing operation parameters
            self._hRpcOper.fill(params=self._cParams.get())

            send_msg = self._hRpcOper.readmsg(self._cParams.get())
            self._cParams.set('messageid', self._cParams.get('messageid')+1)
            self._hConn.sendmsg(send_msg)
            self._cParams.set('sendmsg', send_msg)

            recv_msg = self._hConn.recvmsg()
            self._cParams.set('recvmsg', recv_msg)
            self._hRpcOper.parsemsg(self._cParams.get())
            self._hRpcOper.writemsg(self._cParams.get())

            # reset operation params
            self._cParams.reset()
        except:
            if _operation != 'close-session':
                print 'BNClient: Call sendrpc%s fail' % (' <'+_operation+'>' if len(_operation) else '')
            sys.exit()

        """ end of function exchgmsg """


    def close(self):
        req_msg = "\
<rpc message-id='%d'>\n\
  <close-session/>\n\
</rpc>\n" % self._cParams.get('messageid')
        self._cParams.set('messageid', self._cParams.get('messageid')+1)
        rsp_msg = ''
        try:
            self._hConn.sendmsg(req_msg)
            rsp_msg = self._hConn.recvmsg()
        except:
            pass

        try:
            self._hConn.close()
        except:
            sys.exit()

    """ end of class bnclient """


if __name__ == '__main__':
    bnc = bnclient()
    bnc.connect()
    bnc.sendhello()
    bnc.sendrpc()
    bnc.close()

