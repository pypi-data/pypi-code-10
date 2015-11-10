__author__ = 'Chris Bergh'
import os
import sys
import json
sys.path.insert(0, '../../../../AnalyticMicroService')
import argparse
from collections import OrderedDict
from AnalyticMicroService.server.utils.AMSSingletons import AMSLogger

sample_config = """
{
   "progress": "1"
   "progress": "2"
} \n
    """

"""
the is class does a few things:
    set_config:     get the config passed in, and validates, amd creates prep folder
                    in:     location of interface file mount env variable
                            location requires config.json
    prep:           reads the config, write out the preparation data to the out_dir
    execute:        run based on the config; writes progress.json, tests.json, and logs.txt

"""
class ACExample1(object):

    def __init__(self):
        self.CONTAINER_FILE_MOUNT = "AC_FILE_MOUNT"
        self.configuration = None
        self.config_file_name = 'config.json'
        self.progess_file_name = 'progess.json'
        self.file_mount = os.environ.get(self.CONTAINER_FILE_MOUNT)
        if self.file_mount is not None:
            config_path = os.path.join(self.file_mount, self.config_file_name)
            try:
                with open(config_path) as the_file:
                    self.configuration = json.load(the_file, object_pairs_hook=OrderedDict)
            except ValueError, e:
                s = 'ACExample1:  unable to load config.json  %s %s' % (type(e), e.args)
                AMSLogger.log_and_print_error(s)
        else:
            AMSLogger.log_and_print_error('ACExample1:  unable to open config.json')

    def vaild_config(self):
        if self.configuration is None:
            return False
        else:
            return True

    def print_config(self):
        print json.dumps(self.configuration, indent=4, sort_keys=False)

    def write_progress(self):
        progress_path = os.path.join(self.file_mount, self.progess_file_name)
        # truncate file
        with open(progress_path, 'w') as the_file:
            the_file.write(sample_config)

    @staticmethod
    def execute():
        print 'ACExample1: Executing ....'

def main(parser=None):

    ac_example1 = ACExample1()
    if ac_example1.vaild_config() is True:
        print 'ACExample1: valid config is:'
        ac_example1.print_config()
        print 'ACExample1: writing progress:'
        ac_example1.write_progress()
        try:
            if parser is not None:
                mutually_exclusive_group = parser.add_mutually_exclusive_group()
                mutually_exclusive_group.add_argument('--rude', '-rude', action='store_true', default=False, dest='rude',
                                                      help='Return something rude')
                results = parser.parse_args()
                if results.rude is True:
                    print "ACExample1 ... print rude words\n"

        except argparse.ArgumentError as e:
            s = 'ACExample1:  During processing, caught an unknown exception. type: %s ; args: %s ; message: %s' % (
            type(e), repr(e.args), e.message)
            AMSLogger.log_and_print_error(s)
        except Exception as e:
            s = 'ACExample1:  During processing, caught an unknown exception:  %s %s' % (type(e), e.args)
            AMSLogger.log_and_print_error(s)

        ac_example1.execute()
        AMSLogger.log_and_print('...ACExample1:  Completed command, exiting')
    else:
        print 'ACExample1: Exiting ... invalid config'
        sys.exit()


if __name__ == "__main__":
    cmdline_parser = argparse.ArgumentParser(description="Welcome to the ACExample1 Command Line Program")
    main(cmdline_parser)
