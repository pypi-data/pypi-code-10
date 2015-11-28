# Copyright 2010 Blade Network Technologies

import os, sys, socket

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

from select import select

# ssh library
import paramiko

from rpc import rpc


SSH_DELIMITER = ']]>]]>'


class bnc_conn (object):
    """
    Netconf Connection.
    """

    def __init__(self, params={}, conntype='ssh', timeout=60):
        self._recvbuf = ''
        self._dParams = params
        self._dOperOptions = {}
        self.timeout = timeout
        try:
            self._sHost = self._dParams['hostname']
        except:
            print 'Netconf Connection: Missing hostname!'
            sys.exit()

        try:
            self._uPort = self._dParams['port']
        except:
            print 'Netconf Connection: Missing port!'
            sys.exit()

        try:
            self._sUser = self._dParams['username']
        except:
            print 'Netconf Connection: Missing username!'
            sys.exit()

        try:
            self._sPswd = self._dParams['password']
        except:
            print 'Netconf Connection: Missing password!'
            sys.exit()

        try:
            self._sType = conntype
        except:
            print 'Netconf Connection: Invalid Connection Type'
            sys.exit()

        self._sStatus = 'idle'
        self._iSock = None
        # open socket
        self.opensocket()

    def opensocket(self):
        if self._sStatus == 'idle':
            for res in socket.getaddrinfo(self._sHost, self._uPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                try:
                    self._iSock = socket.socket(af, socktype, proto)
                    self._iSock.settimeout(self.timeout)
                except socket.error:
                    continue
                except:
                    print res
                try:
                    self._iSock.connect(sa)
                except socket.error:
                    self._iSock.close()
                    continue
                self._sStatus = 'opened'
                break
            else:
                print "Netconf Connection: Could not open socket to %s:%s" % (self._sHost, self._uPort)
                sys.exit()
        else:
            print "Netconf Connection: Invalid Status, Could not open socket to %s:%s" % (self._sHost, self._uPort)
            sys.exit()
        return self._iSock
    """ end of function opensocket """

    def connect(self):
        if self._sStatus != 'opened':
            print "Netconf Connection: Invalid Status, Could not connect to %s:%s" % (self._sHost, self._uPort)
            sys.exit()
        # establish ssh connection
        if self._sType == 'ssh':
            # setup transport connection base on socket
            self._hSsh = paramiko.Transport(self._iSock) 
            try:
                self._hSsh.start_client()
            except paramiko.SSHException:
                print 'Netconf Connection: Connect negotiation failed'
                self._iSock.close()
                sys.exit()
            except:
                print 'Netconf Connection: Connect failed'
                try:
                    self._iSock.close()
                except:
                    pass
                sys.exit()
            # auth check
            if self._sPswd != '':
                try:
                    self._hSsh.auth_password(self._sUser, self._sPswd)
                except:
                    print "Netconf Connection: Auth SSH username/password fail"
                    self._iSock.close()
                    sys.exit()
            # open channel for netconf ssh subsystem
            try:
                self._hSshChn = self._hSsh.open_session()
                self._hSshChn.settimeout(5)
                self._hSshChn.set_name("netconf")
                self._hSshChn.invoke_subsystem("netconf")
                self._hSshChn.setblocking(1)
            except:
                print "Netconf Connection: Open SSH Netconf SubSystem fail"
                self._iSock.close()
                sys.exit()
        else:
            print "Netconf Connection: Unsupport Connection Type, Could not connect to %s:%s" % (self._sHost, self._uPort)
            sys.exit()

        self._sStatus = 'connected'

        """ end of function connect """

    def sendmsg(self, data=''):
        if self._sStatus == 'connected' and self._hSshChn.send_ready():
            if self._sType == 'ssh':
                if self._dParams['verbose'] == True:
                    print 'Netconf Connection: SendMsg>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n%s\n' % data
                data += SSH_DELIMITER
                while data:
                    n = self._hSshChn.send(data)
                    data = data[n:]
            else:
                print 'Netconf Connection: Could not send message, Unsupport connection type: %s' % self._sType
                sys.exit()
        else:
            print 'Netconf Connection: Warning: Could not send message'
            sys.exit()

    def recvmsg(self):
        if self._sStatus == 'connected':
            if self._sType == 'ssh':
                while SSH_DELIMITER not in self._recvbuf:
                    try:
                        # waiting for recv message
                        r, w, e = select([self._hSshChn], [], [], 60)
                        if r:
                            self._recvbuf += self._hSshChn.recv(4096)
                        else:
                            self._recvbuf += SSH_DELIMITER
                            break
                    except Exception as e:
                        print 'Netconf Connection: Could not recv message'
                        self._iSock.close()
                        sys.exit()

                try:
                    idx = self._recvbuf.index(SSH_DELIMITER)
                    data = self._recvbuf[:idx]
                    try:
                        self._recvbuf = self._recvbuf[idx+len(SSH_DELIMITER):]
                    except:
                        self._recvbuf = ''
                    if self._dParams['verbose'] == True:
                        print 'Netconf Connection: RecvMsg<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n%s\n' % data
                    return data
                except:
                    print 'Netconf Connection: Could not recv message, Missing SSH delimiter'
                    sys.exit()
            else:
                print 'Netconf Connection: Could not recv message, Unsupport connection type: %s' % self._sType
                sys.exit()
        else:
            print 'Netconf Connection: Warning: Could not recv message'
            sys.exit()


    def close(self):
        try:
            if self._sStatus != 'idle':
                self._iSock.close()
        finally:
            self._sStatus = 'idle'

