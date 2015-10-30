# Copyright 2010 Blade Network Technologies

import os, sys, socket
import getpass

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

from rpc import rpc


# transfer long option to short option
def option_long2short(argv=None, opts={}):
    if argv is not None and len(opts) > 0:
        for arg in argv:
            for opt in opts.values():
                if arg == opt[1] and '--' in arg:
                    argv[argv.index(arg)] = opt[0]


# transfer argv to parameters
def argv2param(argv=[], opts={}, params={}):
    if len(opts) == 0:
        return
    if len(argv) == 0:
        return

    # transfer long option to short option
    option_long2short(argv=argv, opts=opts)

    # fill argv to params
    for opt in opts.items():
        if opt[1][0] in argv:
            try:
                idx = argv.index(opt[1][0])
            except:
                continue
            # check whether need parameter
            if len(opt[1][2]) > 0:
                try:
                    opval = argv[idx:idx+2]
                    params.update({opt[0]:opval[1]})
                    argv.remove(opval[0])
                    argv.remove(opval[1])
                except:
                    print 'Invalid parameter of option \'%s\'' % opt[1][0]
                    sys.exit()
            else:
                try:
                    opval = argv[idx]
                    params.update({opt[0]:True})
                    argv.remove(opval)
                except:
                    print 'Invalid option \'%s\'' % opt[1][0]
                    sys.exit()


class bnc_param(object):
    def __init__(self):
        self._dParams = {
            'username':'',
            'password':'',
            'operation':'',
            'verbose':False,
            'help':False,
            'hostname':'',
            'port':830,
            'messageid':100,
            }


    def get(self, key=None):
        if key is not None:
            try:
                return self._dParams[key]
            except:
                return None
        else:
            return self._dParams


    def set(self, key='', value=None):
        try:
            if len(key) > 0 and value is not None:
                self._dParams.update({key:value})
        except:
            pass

    def reset(self):
        try:
            opts = {}
            if self._dParams.has_key('operation') == True and self._dParams['operation'] in rpc.operations.keys():
                rpc.operations[self._dParams['operation']](opts=opts)
            try:
                for key in opts.keys():
                    self._dParams.pop(key)
            except:
                pass
            try:
                self._dParams.update({
                    'operation':'',
                    'sendmsg':'',
                    'recvmsg':'',
                    'writemsg':'',
                    #'cli_hello':'',
                    #'ser_hello':'',
                    })
            except:
                pass
        except:
            pass


    # parser options
    def parser(self, argv=[], opts={}):
        # parser argv to parameters
        argv2param(argv, opts, self._dParams)

        # check show help
        if self._dParams.has_key('help') == True and self._dParams['help'] == True:
            return

        # parser params['operation']
        if self._dParams.has_key('operation') == True and self._dParams['operation'] in rpc.operations.keys():
            # append operation's options to self._dOptions
            rpc.operations[self._dParams['operation']](opts=opts)
            # parser operation's argv to parameters
            argv2param(argv, opts, self._dParams)

        # parser hostname and port to parameters
        hostport = ''
        if self._dParams.has_key('hostname') == False or self._dParams['hostname'] == '':
            for arg in argv:
                hostport = arg.split(':')
                # fill host
                try:
                    host = socket.gethostbyname(hostport[0])
                except:
                    hostport = ''
                    continue
                if host != '0.0.0.0':
                    self._dParams.update({'hostname':host})
                else:
                    hostport = ''
                argv.remove(arg)
                break
        if (self._dParams.has_key('hostname') == False or self._dParams['hostname'] == '') and hostport != '':
            print '\nUnsolved hostname \'%s\'' % hostport[0]
            sys.exit()

        # file port
        if len(hostport) > 1:
            try:
                port = int(hostport[1])
                if port <= 0 or port > 65535:
                    raise "Invalid port"
                self._dParams.update({'port':port})
            except:
                print '\nInvalid port: %s' % hostport[1]
                sys.exit()


    def fill(self):
        # fill username
        if self._dParams.has_key('username') == False or self._dParams['username'] == '':
            self._dParams.update({'username':raw_input('Enter login name: ')})

        # fill password
        if self._dParams.has_key('password') == False or self._dParams['password'] == '':
            try:
                self._dParams.update({'password':getpass.getpass('Enter login password: ')})
            except:
                self._dParams.update({'password':raw_input('Enter login password: ')})

        # fill hostname and port
        if self._dParams.has_key('hostname') == False or self._dParams['hostname'] == '':
            hostport = raw_input('Enter hostname[:port]: ').split(':')
            try:
                host = socket.gethostbyname(hostport[0])
                self._dParams.update({'hostname':host})
            except:
                print '\nInvalid hostname: %s' % hostport[0]
                sys.exit()
            if len(hostport) > 1:
                try:
                    port = int(hostport[1])
                    if port<= 0 or port > 65535:
                        raise "Invalid port"
                    self._dParams.update({'port':port})
                except:
                    print '\nInvalid port: %s' % hostport[1]
                    sys.exit()

