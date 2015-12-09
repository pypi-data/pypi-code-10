#!/usr/bin/python

import subprocess
import signal
import threading
import sys
import logging

signalNames = {}
for sigName, sigVal in filter(lambda x:x[0].startswith("SIG"), vars(signal).iteritems()) :
    signalNames[sigVal] = sigName

class InitLauncher(object) :
    methods = {
        "SIGINT" : "stop",
        "SIGTERM" : "stop",
        "SIGHUP" : "reload",
        "SIG_IGN" : "reload",
    }
    def handler(self, signum, *args) :
        orig = self.origSignals[signum]
        if self.callInitScript(self.methods.get(signalNames[signum], signalNames[signum])) != 0 :
            self.logger.error("failed to run init script, exiting")
            self.runing = False
        if signum in( signal.SIGINT, signal.SIGTERM, ) :
            self.logger.debug("received SIGINT, exiting listener")
            self.running = False
    def __init__(self, initScript, **kwds) :
        self.logger = logging.getLogger(self.__class__.__name__)
        self.origSignals = {}
        self.running = True
        self.initScript = initScript
        self.methods = dict(self.methods)

        for key,val in kwds.iteritems() :
            self.logger.debug("mapping %s to %s init method", key, val)
            self.methods[key] = val

        for sigVal, sigName in signalNames.iteritems() :
            if sigName in ("SIG_DFL", "SIGTTOU", "SIGKILL", "SIGSTOP", "SIGCLD") : continue
            self.origSignals[sigVal] = signal.signal(sigVal,self.handler)

    def callInitScript(self, method) :
        if method is None :
            return 0
        self.logger.debug("calling init script %r", [self.initScript, method])
        return subprocess.Popen([self.initScript, method], stderr=subprocess.STDOUT).wait()

    def start(self) :
        if self.callInitScript("start") == 0 :
            while self.running :
                signal.pause()

def main() :
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-i", "--init", dest="init", default=None,
                      help="the SCRIPT be started / stopped / .... (in /etc/init.d when relative)", metavar="SCRIPT")
    for sig in signalNames.values():
        parser.add_option("--%s"%sig, dest=sig, default=None,
                          help="the ACTION to be performed on SCRIPT when %s signal is received (start, stop, graceful, reload, ...)"%sig, metavar="ACTION")
    
    (options, args) = parser.parse_args()

    launcherArgs = {}
    for sig in signalNames.values():
        action = getattr(options, sig)
        if action is not None :
            launcherArgs[sig] = action
    InitLauncher(options.init, **launcherArgs).start()
    

if __name__ == "__main__" :
    main()

