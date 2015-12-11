# -*- coding: utf-8 -*-

import random
import zmq
import sys
import time
import json
import importlib
import imp
import abc
from datetime import datetime
from six import with_metaclass

from keystone.strategy import KSStrategy, KSStrategyRunner
from keystone.sources import KSCsvSource
from keystone.performance.analyzer import KSDefaultAnalyzer, KSCumulativeAnalyzer
from keystone.app_client.kpdb import KPdb

from keystone.app_client.session import Session
from keystone.app_client.json_utils import json_clean
from keystone.py3compat import PY3, builtin_mod

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


'''
StrategyClient

Run backtesting using a config
config format:
{
    "in_url": string, stdin url for ipc, e.g. "tcp://127.0.0.1:55555",
    "drain_url": string, drain url for ipc, e.g. "tcp://127.0.0.1:55556",
    "session": string, uuid,
    "filename": "/Users/rk/Desktop/share_folder/keystone-strategy-engine/node/strategy.py",
    "stratingCash": int, 100000,
    "startTime": string, 
    "endTime": string,
    "stopPercentage": float, in [0.0,1.0],
    "historyCapacity": int, history capacity,
    "instanceMatch": bool,
    "analyzer": ['alpha', 'beta', ...]
    "sources": [
        {"type": "csv",
         "path": "/Users/rk/Desktop/share_folder/keystone-strategy-engine/data/market.csv",
         "dt_column": "dt",
         "dt_format": "%Y-%m-%d %H:%M:%S",
         "price_column": "price",
         "sid_column": "sid",
         "delimiter": ","}, ..., ...]
 }
'''
class StrategyClient(with_metaclass(abc.ABCMeta)):
    # outstream_factory = OutStream
    # outstream_factory.flush_interval = 0.0
    session = Session()
    context = zmq.Context()
    def __init__(self, config):
        if isinstance(config, basestring):
            config = json.loads(config)
        elif isinstance(config, dict):
            config = dict(config)
        else:
            raise TypeError("input config MUST BE 'string' or 'dict'")
        self.config = byteify(config)
        self.check_config(config)
        self.strategy_runner = KSStrategyRunner()

        self.init_session()
        self.init_strategy()
        self.init_strategy_runner()
        self.init_socket()
        if not config.has_key('io_redircet') or config['io_redircet'] == True:
            self.io_redirect()

    def check_config(self, config):
        pass

    def init_session(self):
        self.session.auth = None
        if self.config.has_key('session'):
            Session.session = self.config['session']
        self.session_uuid = Session.session

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
                self.strategy_runner.addSource(source)
            # use user strategy class
            self.strategy_runner.useStrategy(self.strategy)
            # history
            if config.has_key("historyCapacity"):
                self.strategy_runner.setHistoryCapacity(config["historyCapacity"])
            # start time and end time
            if config.has_key("startTime"):
                dt = datetime.strptime(config["startTime"], '%Y-%m-%d %H:%M:%S')
                self.strategy_runner.setStartTime(dt)
            if config.has_key("endTime"):
                dt = datetime.strptime(config["endTime"], '%Y-%m-%d %H:%M:%S')
                self.strategy_runner.setEndTime(dt)
            # analyzer
            default_analyzer = KSDefaultAnalyzer()
            self.strategy_runner.attachAnalyzer(default_analyzer)
            # stop percentage
            if config.has_key("stopPercentage"):
                self.strategy_runner.setStopPercentage(config["stopPercentage"])
            # drain address
            if config.has_key("drain_url") and config.has_key("syn_url"):
                self.strategy_runner.setDrainAddress(config["drain_url"], config["syn_url"])
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
            if source_config.has_key('delimiter'):
                source.setDelimiter(source_config['delimiter'])
            return source
        else:
            raise ValueError("cannot support source type \"%s\""%(src_type))

    def init_socket(self):
        config = self.config
        stdin_socket = self.context.socket(zmq.DEALER)
        # stdin_socket.linger = 1000
        stdin_socket.setsockopt(zmq.IDENTITY, self.session_uuid.encode('utf8'))
        stdin_socket.connect(config['in_url'])
        self.stdin_socket = stdin_socket

        # following code is moved to drain.py
        # stdout_socket = self.context.socket(zmq.PUB)
        # stdout_socket.linger = 1000
        # stdout_socket.bind(config['drain_url'])
        # self.stdout_socket = stdout_socket

    def io_redirect(self):
        self._forward_input()
        # sys.stdout = self.outstream_factory(self.session, self.stdout_socket, u'stdout')
        # sys.stderr = self.outstream_factory(self.session, self.stdout_socket, u'stderr')

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
        msg = self.session.send(self.stdin_socket, u'input_request', content = content)
        # print >>sys.stderr, "sending input request: " + msg.__str__()

        # Await a response.
        while True:
            try:
                # print >>sys.stderr, "waiting..."
                ident, reply = self.session.recv(self.stdin_socket,0)
                # print >>sys.stderr, "*********ident(%s), recieve %s"%(ident, reply)
            except Exception as e:
                print >>sys.stderr, "Invalid Message"
                raise e
            except KeyboardInterrupt:
                # re-raise KeyboardInterrupt, to truncate traceback
                raise KeyboardInterrupt
            else:
                break
        try:
            value = reply['content']['value'].encode('utf8', "replace")
        except:
            print >>sys.stderr, "Bad input_reply"
            # self.log.error("Bad input_reply: %s", parent)
            value = ''
        if value == '\x04':
            # EOF
            raise EOFError
        return value

    @abc.abstractmethod
    def run(self, config):
        pass

class StrategyRunner(StrategyClient):
    def run(self):
        self.strategy_runner.run()
        # import pdb
        # my_pdb = pdb.Pdb(stdout=sys.stdout);
        # my_pdb.use_rawinput = True
        # self.my_pdb = my_pdb
        # my_pdb.do_break('/Users/rk/Desktop/share_folder/keystone-strategy-engine/node/example.py:17')
        # my_pdb.do_break('/Users/rk/Desktop/share_folder/keystone-strategy-engine/node/example.py:17')
        # my_pdb.do_break('/Users/rk/Desktop/share_folder/keystone-strategy-engine/node/example.py:17')
        # my_pdb.do_break('/Users/rk/Desktop/share_folder/keystone-strategy-engine/node/example.py:18')
        # my_pdb.runeval('self.strategy_runner.run()', globals(), locals())

class StrategyDebugger(StrategyClient):
    def __init__(self, *args, **kwargs):
        StrategyClient.__init__(self, *args, **kwargs)
        # set drain to debug mode
        # self.strategy_runner.drain.send_data = True

        # initialize KPdb
        self.pdb = KPdb(self.session, 
            self.config['notify_url'], 
            self.config['syn_url'], 
            datetime_break_func=self.strategy_runner.strategyInstance.onData,
            datetime_break_cond="self._datetimeBreakPointCls.is_break_at_datetime(data.time())",
            current_time_func=self.strategy_runner.universe.time,
            stdout=sys.stdout);
        self.pdb.use_rawinput = True

        # set datetime break point condition
        # err = self.pdb.do_break_at_function(self.strategy_runner.strategyInstance.onData, 
        #     cond = "self._datetimeBreakPointCls.is_break_at_datetime(data.time())")
        # if err:
        #     print >>sys.stderr, err
        # self.pdb.onecmd('')

    def execute_cmd(self, cmds):
        for cmd in cmds:
            self.pdb.onecmd(cmd)

    def run(self):
        self.pdb.run('self.strategy_runner.run()', globals(), locals())


