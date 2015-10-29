import argparse
import json
from egat.loggers.test_logger import LogLevel

class ParseError(Exception):
    pass

class ConfigurationValidator():
    @staticmethod
    def validate_config_json(pjson):
        """Takes the parsed JSON (output from json.load) from a configuration file 
        and checks it for common errors."""
        # Make sure that the root json is a dict
        if type(pjson) is not dict:
            raise ParseError("Configuration file should contain a single JSON object/dictionary. Instead got a %s." 
                             % type(pjson))

        # if 'configuration' is present it should be a dict of strings and numbers.
        # The ArgumentParser will do the rest of the validation.
        configuration = pjson.get('configuration', {})
        if type(configuration) is not dict:
            raise ParseError('''"configuration" object should be a dict, got %s instead.''' 
                             % type(configuration))

        # Make sure that the 'tests' key is present 
        try:
            tests = pjson["tests"]
        except KeyError:
            raise KeyError("Configuration file requires 'tests' attribute.")

        # Verify that 'options' is a dict if present
        options = pjson.get('options', {})
        if type(options) is not dict:
            raise ParseError('"options" attribute must be a dictionary"')

        # We need to know whether --user-defined-threads option is present to do 
        # the rest of the validation.
        if '-u' in options.keys() or '--user-defined-threads' in options.keys():
            ConfigurationValidator.validate_user_threaded_json(pjson)
        else:
            ConfigurationValidator.validate_auto_threaded_json(pjson)

    @staticmethod
    def validate_user_threaded_json(pjson):
        """Takes a parsed JSON dict representing a set of tests in the user-threaded 
        format and validates it."""
        tests = pjson["tests"]

        # Verify that 'tests' is a two dimensional list
        is_2d_list = lambda ls: len(ls) == len(filter(lambda l: type(l) is list, ls))
        if type(tests) is not list or not is_2d_list(tests):
            raise ParseError("'tests' should be a two-dimensional list of strings when '--user-defined-threads' is present.")

        # Verify that 'tests' sub-lists are of strings
        for sublist in tests:
            for test in sublist:
                if type(test) is not unicode:
                    raise TypeError(
                        "Expected a unicode string but got %s. 'tests' should be a two-dimensional list of strings when '--user-defined-threads is present.'" 
                        % test
                    )

        # Verify that 'environments' key is not present
        try:
            pjson["environments"]
            raise ParseError("'environments' list is not allowed when --user-defined-threads is present.")
        except KeyError: pass


    @staticmethod
    def validate_auto_threaded_json(pjson):
        """Takes a parsed JSON dict representing a set of tests in the auto-threaded
        format and validates it, descending recursively if necessary."""
        # pjson should be a dict or unicode
        if not type(pjson) is dict:
            raise ParseError("Expected a JSON object/dictionary or a string representing a test. Instead got %s." 
                             % pjson)

        # Make sure that the 'tests' key is present 
        try:
            tests = pjson["tests"]
        except KeyError:
            raise KeyError("Test object requires 'tests' attribute.\nObject: %s" % 
                           json.dumps(pjson))

        # Verify that tests is a list
        if type(tests) is not list:
            raise ParseError(
                "Expected 'tests' to be a list but got object of type %s.\nObject: %s" %
                (type(tests), json.dumps(tests))
            )

        # Verify that 'options' is a dict if present
        options = pjson.get('options', {})
        if type(options) is not dict:
            raise ParseError('"options" attribute must be a dictionary')

        # Verify that 'environments' is a list of dicts if present
        environments = pjson.get('environments', [])
        is_list_of_dicts = lambda ls: len(ls) == len(filter(lambda d: type(d) is dict, ls))
        if type(environments) is not list or not is_list_of_dicts(environments):
            raise ParseError('"environments" attribute must be a list of dictionaries. Instead got %s.' % environments)

        for test in tests:
            if type(test) is unicode:
                # Base case for recursion
                pass
            else:
                # Recur
                ConfigurationValidator.validate_auto_threaded_json(test)

class ArgumentParser():
   """A custom argument parser used to parse the command-line arguments or
   configuration file for the TestRunner. This ArgumentParser uses an interface
   similar to argparse.ArgumentParser but is not a strict subclass of it."""

   def __init__(self):
      # Define arguments
      parser = argparse.ArgumentParser(
         description="A command-line client for running functional test scripts.",
      )
      self.parser = parser

      parser.add_argument(
         "-l",
         "--log",
         metavar="LOG_DIR",
         help="""A path specifying the directory where the log should be written
              instead of STDOUT. If this option is present, test output will be
              generated by the HTMLLogger.""",
      )

      parser.add_argument(
         "-c",
         "--config",
         metavar="CONFIG_FILE",
         help="""A configuration file which can be used to specify longer lists of
         tests and supports additional features. If this flag is present all other
         flags on the command line will be ignored.""",
      )

      parser.add_argument(
         "-t",
         "--number-of-threads",
         metavar="NUMBER_OF_THREADS",
         type=int,
         default=1,
         help="""An integer specifying the number of threads the tests should be run
         in. Defaults to 1. Only valid if --user-defined_threads is not present.""",
      )

      parser.add_argument(
          "-u",
          "--user-defined-threads",
          action='store_true',
          help="""A flag that signals that the user has defined which tests should
          run in which threads in the configuration file. Only valid in a
          configuration file."""
      )

      parser.add_argument(
         "--log-level",
         metavar="LOG_LEVEL",
         choices=["DEBUG", "INFO", "ERROR"],
         default="ERROR",
         help="Sets the log level. Valid values are ERROR, INFO, and DEBUG. Defaults to ERROR.",
      )

      parser.add_argument(
         'tests',
         type=str,
         nargs='*',
         help="""The fully qualified package, module, class, or function names of the
         test you wish to run."""
      )

      parser.add_argument(
          '--css-path',
          type=str,
          help="""An optional css file to be used with the HTMLLogger instead of the
          default one."""
      )

   def parse_args(self):
      """Parses the command-line arguments to this script, and parse the given
      configuration file (if any).  Returns a Namespace containing the resulting
      options. This method will use the configuration file parameters if any exist,
      otherwise it will use the command-line arguments."""
      # Parse sys.argv
      cli_args = self.parser.parse_args()

      if cli_args.config:
         # Parse the configuration file
         config_file = open(cli_args.config, 'r')
         config_json = json.load(config_file)
         config_opts = config_json.get('options', {})

         # Validate the configuration file
         ConfigurationValidator.validate_config_json(config_json)

         # Turn JSON options into a flat list of strings for the parser
         args = reduce(lambda l, t: l + [str(t[0]), str(t[1])], config_opts.items(), [])
         args = filter(lambda x: x is not None, args)

         # Pass the configuration file options to the parser
         config_args = self.parser.parse_args(args=args)
         config_args.tests = config_json.get('tests', [])
         config_args.configuration = config_json.get('configuration', {})
         config_args.environments = config_json.get('environments', [])

         args = config_args
      else:
         args = cli_args

      
      if args.log_level == "INFO":
          args.log_level = LogLevel.INFO
      elif args.log_level == "WARN":
          args.log_level = LogLevel.WARN
      elif args.log_level == "DEBUG":
          args.log_level = LogLevel.DEBUG
      else:
          args.log_level = LogLevel.ERROR

      return args
