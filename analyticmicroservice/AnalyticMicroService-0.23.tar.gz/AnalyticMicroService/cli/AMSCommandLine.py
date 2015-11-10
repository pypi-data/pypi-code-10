__author__ = 'Chris Bergh'
import sys
if not '../' in sys.path:
    sys.path.insert(0, '../')

import argparse
from modules.AMSCommandRunner import AMSCommandRunner
from modules.AMSCommandRunnerConfig import AMSCommandRunnerConfig
from server.utils.AMSSingletons import *

sample_config = """
    Sample AMSCommandLineConfig.json
        {
           "ams-ip": "127.0.0.1"
           "ams-port": "14001"
        }
            """

def main(parser, config_json_path='./AMSCommandLineConfig.json'):

    try:
        command_line_config = AMSCommandRunnerConfig()
        if command_line_config.init_from_file(config_json_path) is False:
            print 'ERROR AMSCommandLine.py Requires a AMSCommandLineConfig.json '
            print sample_config
            exit()

        command_runner = AMSCommandRunner(command_line_config)
        mutually_exclusive_group = parser.add_mutually_exclusive_group()

        mutually_exclusive_group.add_argument('--rude', '-rude', action='store_true', default=False, dest='rude',
                                              help='Return something rude')

        mutually_exclusive_group.add_argument('--images', '-images', action='store_true', default=False, dest='images',
                                              help='Return a list of images')

        mutually_exclusive_group.add_argument('--endtoend', '-endtoend', action='store_true', default=False, dest='endtoend',
                                              help='Return a endtoend REST call')

        mutually_exclusive_group.add_argument('--search', '-search', action='store', default=False, dest='search_string',
                                              help='Return a list of images for <search string>')
        other_stuff_group = parser.add_argument_group()

        other_stuff_group.add_argument('--tag', '-tag', action='store', dest='tag',
                                       help='Useful for finding the process in the process list')

        results = parser.parse_args()

        if results.rude is True:
            rude = command_runner.rude()
            if rude is None:
                AMSLogger.log_and_print_error('AMSCommandRunner().rude() failed')
            else:
                print "AMSCommandRunner().rude() = %s\n" % rude
        elif results.images is True:
            images = command_runner.images()
            if images is None:
                AMSLogger.log_and_print_error('AMSCommandRunner().images() failed')
            else:
                print "AMSCommandRunner().images()\n"
                for image in images:
                    print "%s \n" % image
        elif results.endtoend is True:
            endtoend = command_runner.get_end_to_end()
            if endtoend is None:
                AMSLogger.log_and_print_error('AMSCommandRunner().endtoend() failed')
            else:
                print "AMSCommandRunner().endtoend() = %s" % endtoend
        elif results.search_string is not None:
            sr = command_runner.search(results.search_string)
            if sr is None:
                AMSLogger.log_and_print_error('AMSCommandRunner().search() failed')
            elif len(sr) == 0:
                print "found none"
            else:
                for s in sr:
                    print "%s \n" % s
        else:
            parser.print_help()

    except argparse.ArgumentError as e:
        s = 'AMSCommandLine:  During processing, caught an unknown exception. type: %s ; args: %s ; message: %s' % (
        type(e), repr(e.args), e.message)
        AMSLogger.log_and_print_error(s)
    except Exception as e:
        s = 'AMSCommandLine:  During processing, caught an unknown exception:  %s %s' % (type(e), e.args)
        AMSLogger.log_and_print_error(s)
    except:
        s = 'AMSCommandLine:  During processing, caught an unknown exception. %s' % sys.exc_info()[0]
        AMSLogger.log_and_print_error(s)

    AMSLogger.log_and_print('...AMSCommandLine:  Completed command, exiting')


if __name__ == "__main__":
    cmdline_parser = argparse.ArgumentParser(description="Welcome to the Analytic MicroService Command Line Program")
    main(cmdline_parser)
