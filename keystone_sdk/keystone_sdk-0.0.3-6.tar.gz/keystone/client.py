# -*- coding: utf-8 -*-

import random
import zmq
import sys
import time
import json
import importlib
import imp

from keystone.strategy import KSStrategy, KSStrategyRunner
from keystone.sources import KSCsvSource
from keystone.performance.analyzer import KSDefaultAnalyzer, KSCumulativeAnalyzer

from ipykernel.iostream import OutStream
from ipykernel.jsonutil import json_clean
from ipython_genutils import py3compat
from ipython_genutils.py3compat import builtin_mod, PY3
from jupyter_client.session import Session
from traitlets import (
            Any, Instance, Float, Dict, List, Set, Integer, Unicode, Bool,
            )

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--config', help='strategy config', required=True)

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class StrategyClient(object):
    outstream_factory = OutStream
    session = Session()
    session.auth = None
    context = zmq.Context()
    def __init__(self, config):
        if isinstance(config, basestring):
            config = json.loads(config)
        self.config = byteify(config)
        self.check_config(config)
        self.strategy_runner = KSStrategyRunner()
        self.init_strategy()
        self.init_strategy_runner()
        self.init_socket()
        self.io_redirect()

    def check_config(self, config):
        pass

    def init_strategy(self):
        try:
            module = imp.load_source('UserStrategy', self.config['filename'])
            self.strategy = module.MyStrategy()
        except Exception as e:
            raise ValueError("cannot find MyStrategy class in %s"%(self.config['filename']))

    def init_strategy_runner(self):
        config = self.config
        try:
            # init source
            sources = config['sources']
            for source_config in sources:
                source = self._get_source(source_config)
                # print >>sys.stderr,source
                self.strategy_runner.addSource(source)
            # analyzer
            cumulative_analyzer = KSCumulativeAnalyzer()
            self.strategy_runner.attachAnalyzer(cumulative_analyzer)
            # use user strategy class
            self.strategy_runner.useStrategy(self.strategy)
            # history
            self.strategy_runner.setHistoryCapacity(10)
        except Exception as e:
            raise ValueError("Initilize strategy config error: %s"%(e))

    def _get_source(self, source_config):
        src_type = source_config['type'].lower()
        if source_config['type'].lower() == "csv":
            source = KSCsvSource(source_config['path'], source_config['dt_column'], source_config['dt_format'])
            # price data or security data
            if source_config.has_key('sid_column'):
                if source_config.has_key('price_column'):
                    source.tagAsPriceData(source_config['sid_column'], source_config['price_column'])
                else:
                    source.tagAsSecurityData(source_config['sid_column'])
            # delimiter
            return source
        else:
            raise ValueError("cannot support source type \"%s\""%(src_type))

    def init_socket(self):
        config = self.config
        stdin_socket = self.context.socket(zmq.DEALER)
        stdin_socket.linger = 1000
        stdin_socket.connect(config['in_url'])
        self.stdin_socket = stdin_socket

        stdout_socket = self.context.socket(zmq.PUB)
        stdout_socket.linger = 1000
        stdout_socket.bind(config['out_url'])
        self.stdout_socket = stdout_socket
        # if identity:
            # sock.identity = identity

    def io_redirect(self):
        self._forward_input()
        sys.stdout = self.outstream_factory(self.session, self.stdout_socket, u'stdout')

    def _forward_input(self):
        if PY3:
            self._sys_raw_input = builtin_mod.input
            builtin_mod.input = self.raw_input
        else:
            self._sys_raw_input = builtin_mod.raw_input
            self._sys_eval_input = builtin_mod.input
            builtin_mod.raw_input = self.raw_input
            builtin_mod.input = lambda prompt='': eval(self.raw_input(prompt))

    def raw_input(self, prompt=''):
        """Forward raw_input to frontends
        Raises
        ------
        StdinNotImplentedError if active frontend doesn't support stdin.
        """
        return self._input_request(prompt, password=False)

    def _input_request(self, prompt, password=False):
        # Flush output before making the request.
        sys.stderr.flush()
        sys.stdout.flush()
        # flush the stdin socket, to purge stale replies
        while True:
            try:
                self.stdin_socket.recv_multipart(zmq.NOBLOCK)
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    break
                else:
                    raise

        # Send the input request.
        content = json_clean(dict(prompt=prompt, password=password))
        msg = self.session.send(self.stdin_socket, u'input_request', content)
        print >>sys.stderr, "sending input request: " + msg.__str__()

        # Await a response.
        while True:
            try:
                # print >>sys.stderr, "waiting..."
                ident, reply = self.session.recv(self.stdin_socket, 0)
                print >>sys.stderr, "recieve %s"%(reply)
            except Exception as e:
                print >>sys.stderr, "Invalid Message"
                raise e
            except KeyboardInterrupt:
                # re-raise KeyboardInterrupt, to truncate traceback
                raise KeyboardInterrupt
            else:
                break
        try:
            value = py3compat.unicode_to_str(reply['content']['value'])
        except:
            print >>sys.stderr, "Bad input_reply"
            # self.log.error("Bad input_reply: %s", parent)
            value = ''
        if value == '\x04':
            # EOF
            raise EOFError
        return value

    def run(self):
        self.strategy_runner.run()
        # import pdb

# if __name__ == "__main__":
#     args = parser.parse_args()
#     runner = PythonSDKRunner(args.config)
#     runner.run()
