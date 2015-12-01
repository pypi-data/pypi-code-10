import configparser
import getopt
import sys
import traceback

from .error import ConfigVarNotDefinedError, ConfigSchemaError, CLISchemaError, ConfigFileNotFoundError, \
    ConfigValueError, PyfiguratorError
from .cli_options import CLIOptionsSet


class Config(object):
    """
    A :class:`.Config` object is the defacto interface for run-time configurations in pyfigurator.

    :class:`.Config` objects generally go through the following life-cycle:
        1. The :class:`.Config` object is constructed based on a given schema and a CLI schema that defines a set of
           command line arguments and maps them to the configuration.
        #. Command line arguments are parsed with :meth:`.parseCommandLineArgs`.
        #. A config file is parsed with :meth:`.parseConfigFile`.
        #. The configuration is validated to ensure all required configuration objects have been set.

    Note that it does not matter if the command line arguments or the config file is called first, but if you wish
    to allow a config file to be specified via the CLI, then command line arguments must be processed first.

    Pyfigurator supports INI style config files.  The schema is defined by a JSON-style dict as defined below:

    .. code-block:: python

        {'MySection': {'MyStrVar': {'name': 'my_str_var', 'type': str, 'required': True, 'default': None},
                       'MyBoolVar': {'name': 'my_bool_var', 'type': bool, 'required': False, 'default': True},
                      }
         'MyOtherSection: {'MyIntVar': {'name': 'my_int_var', 'type': int, 'required': False, 'default': None},
        }

    The following is a sample INI file for the above schema:

    .. code-block:: none

        [MySection]
        MyStrVar: This is a String
        MyBoolVar: yes

        [MyOtherSection]
        MyIntVar: 42

    As you can see, the schema JSON follows the general definition path of *Section -> Name -> Definition*.

    .. note:: INI File Syntax:

        Pyfigurator uses :module:`configparser` as a backend.  See its documentation for more information on INI
        file syntax.

    The definition is a set of parameters that describe the intent of the configuration variable:

        - **name** (:class:`str`) -- The internal name of the variable (as it is accessed from the :class:`.Config` object.
        - **type** (:class:`type`) -- The expected type of the variable.  Supported types are :class:`str`, :object:`bool`, :object:`int`, and :object:`float`.
        - **required** (:object:`bool`) -- Whether or not this variable can be ``None``.
        - **default** (*mixed*) -- A default value for the variable.  This can be ``None``.  If **required** is True, then setting this to something other than ``None`` will obviously satisfy that requirement.

    After the :class:`.Config` object has been created, you can access and modify these variables as attributes of
    the :class:`.Config`.  For instance, we can set the *MyStrVar* variable from the *MySection* section in our
    internal :class:`.Config` with ``myConfig.my_str_var = "the new str value"``.  We can get that value back with
    ``myConfig.my_str_var``.

    Of course, we'd usually just call :meth:`.parseCommandLineArgs` and :meth:`.parseConfigFile` first.

    The Command Line Interface (CLI) is defined through a CLI Schema.  The CLI schema must contain a subset of the
    configuration attributes defined in the Config Schema.  It may not contain attributes not defined in the Config
    Schmea.

    Here is an example CLI Schema for our example Config Schema:

    .. code-block:: python

        {'mybool': {'takesArg': False,
                    'help': 'An example help message for my_bool_var (--mybool)',
                    'name': 'my_bool_var',
                    'val': True,
                    'aliases': ('b'),
                   },
         'mystr': {'takesArg': True,
                   'help': 'An example help message for my_str_var (--mystr arg)',
                   'name': 'my_str_var',
                  },
        }

    Again, the schema is defined as a JSON-like object.  The keys in the outer-most dictionary are the main option text.
    They can be short-form single letter options or long-form strings. They are further defined by a dict that specifies
    the following parameters:

        - **takesArg** (:object:`bool`) -- Specifies whether this option takes an argument or whether it is just a flag.
        - **help** (:class:`str`) -- An explanation of the CLI option's use (used by :meth:`.getCLIUsageMessage`)
        - **name** (:class:`str`) -- The configuration attribute that this option maps to.
        - **val** (*mixed*) -- If this is a flag option (``takesArg == False``), what should the value be set as if the flag is asserted?
        - **aliases** (*tuple[str]*) -- Aliases for this option. You can specify any number of them, but they cannot conflict with other aliases or names.  This is optional.
    """
    _VALID_TYPES = (str, bool, int, float)

    def __init__(self, applicationName, cfgSchema, cliSchema, usageExitCode=64):
        """
        :param applicationName: The name of the application being configured (used in :meth:`.getCLIUsageMessage`)
        :type applicationName: str
        :param cfgSchema: A JSON-like representation of the Configuration.
        :type cfgSchema: dict[str, dict[str, dict[str, mixed]]]
        :param cliSchema: A JSON-like representation of the Command Line Interface.
        :type cliSchema: dict[str, dict[str, mixed]]
        :param usageExitCode: The code to exit with if the user misuses the CLI.
        :type usageExitCode: int

        :raises:
            :exc:`.ConfigSchemaError`
            :exc:`.CLIDuplicateOptionException`
            :exc:`.CLISchemaError`
        """
        self.applicationName = applicationName
        self._sourceFileLocation = None
        self._usageExitCode = usageExitCode

        # Process cfgSchema
        self._types = {}
        self._configFileMap = {}
        self._isRequired = {}
        self._defaults = {}
        self._varName2ConfigPath = {}
        self._options = {}

        try:
            for section, sectionDef in cfgSchema.items():
                self._configFileMap[section] = {}
                for cfgVarName, cfgVarDef in sectionDef.items():
                    if cfgVarDef['type'] not in self._VALID_TYPES:
                        raise ConfigSchemaError()

                    if cfgVarDef['default'] is not None and not isinstance(cfgVarDef['default'], cfgVarDef['type']):
                        raise ConfigSchemaError()

                    self._configFileMap[section][cfgVarName] = cfgVarDef['name']
                    self._types[cfgVarDef['name']] = cfgVarDef['type']
                    self._isRequired[cfgVarDef['name']] = cfgVarDef['required']
                    self._defaults[cfgVarDef['name']] = cfgVarDef['default']
                    self._varName2ConfigPath[cfgVarDef['name']] = (section, cfgVarName)

                    # We only want to add valid options if they are specified.
                    try:
                        self._options[cfgVarDef['name']] = cfgVarDef['select']
                    except KeyError:
                        pass

                    self.__setattr__(cfgVarDef['name'], cfgVarDef['default'])
        except KeyError:
            raise ConfigSchemaError()

        # Process cliSchema
        self._cliOptionsSet = CLIOptionsSet()
        try:
            for optionName, optionDef in cliSchema.items():
                takesArg = optionDef['takesArg']
                helpMsg = optionDef['help']
                varName = optionDef['name']

                try:
                    type = self._types[varName]
                except KeyError:
                    type = optionDef['type']

                val = None
                if not takesArg:
                    val = optionDef['val']

                if val is not None and not isinstance(val, type):
                    raise CLISchemaError()

                try:
                    aliases = optionDef['aliases']
                except KeyError:
                    aliases = []

                self._addCLIOption(optionName, takesArg, helpMsg, varName, type, aliases, val)
        except KeyError:
            raise CLISchemaError()

    def __setattr__(self, name, val):
        isValidValue = True
        try:
            isValidValue = val in self._options[name]
        except (KeyError, AttributeError):
            pass

        if isValidValue:
            self.__dict__[name] = val
        else:
            raise ConfigValueError()

    def __repr__(self):
        return repr(self.__dict__)

    def __str__(self):
        confVars = {}
        for attr, val in self.__dict__.items():
            if attr[0] != '_':
                confVars[attr] = val

        return str(confVars)

    def _addCLIOption(self, name, takesArg, helpMsg, varName, type, aliases, flagVal):
        self._cliOptionsSet.addOption(name, takesArg, helpMsg, varName, type, aliases, flagVal)

    def parseConfigFile(self, cfgFilePath, override=False, checkRequired=True):
        """
        Open the given file, and set the configuration options based on its contents.

        :param cfgFilePath: The relative or absolute path to the config file.
        :type cfgFilePath: str
        :param override: When true, the config file takes precedence over the current configuration.
        :type override: bool
        :param checkRequired: If true, runs :meth:`.checkRequired` after parsing the command lines.
        :type checkRequired: bool

        :raises:
            :exc:`.ConfigFileNotFoundError`
            :exc:`.ConfigValueError`
            :exc:`.ConfigVarNotDefinedError`
            :exc:`.PyfiguratorError`

        """
        self._sourceFileLocation = cfgFilePath

        try:
            config = configparser.ConfigParser()
            if not config.read(cfgFilePath):
                raise ConfigFileNotFoundError()

            for section, sectionVarList in self._configFileMap.items():
                for cfgVarName, varName in sectionVarList.items():
                    try:
                        val = self.__getattribute__(varName)

                        if val is not None and not override:
                            continue
                    except AttributeError:
                        pass

                    try:
                        if self._types[varName] is str:
                            val = config.get(section, cfgVarName, fallback=self._defaults[varName])
                        elif self._types[varName] is bool:
                            val = config.getboolean(section, cfgVarName, fallback=self._defaults[varName])
                        elif self._types[varName] is int:
                            val = config.getint(section, cfgVarName, fallback=self._defaults[varName])
                        elif self._types[varName] is float:
                            val = config.getfloat(section, cfgVarName, fallback=self._defaults[varName])

                        self.__setattr__(varName, val)
                    except Exception as e:
                        raise e
        except ValueError:
            raise ConfigValueError()
        except PyfiguratorError as e:
            raise e
        except Exception as e:
            raise PyfiguratorError(traceback.format_exc(e))

        if checkRequired:
            self.validateRequired()

    def parseCommandLineArgs(self, argv, checkRequired=False):
        """
        Configure based on the given command line arguments.

        If the parse itself fails, then pyfigurator will print a formatted usage statement and exit with the exit code
        specified when the :class:`.Config` object was created.

        .. Note:: Strange long opt behavior:

            **From the :meth:`getopt.getopt` documentation:**

             Long options on the command line can be recognized so long as they provide a prefix of the option name that
             matches exactly one of the accepted options. For example, if longopts is ['foo', 'frob'], the option --fo
             will match as --foo, but --f will not match uniquely, so GetoptError will be raised.

        :param argv: The command line arguments (sys.argv[1:])
        :type argv: list[str]
        :param checkRequired: If true, runs :meth:`.checkRequired` after parsing the command lines.
        :type checkRequired: bool

        :return: A list of the remaining args (the leftovers after the options are processed).
        :rtype: list[str]

        :raises:
            :exc:`.ConfigVarNotDefinedError`
            :exc:`SystemExit`
        """
        shortOpts, longOpts = self._cliOptionsSet.getOptionsLists(shortOptsAsString=True)
        
        try:
            opts, args = getopt.getopt(argv, shortOpts, longOpts)

            for opt, arg in opts:
                varName, val = self._cliOptionsSet.processOptionInput(opt, arg)
                self.__setattr__(varName, val)
        except (getopt.GetoptError, PyfiguratorError):
            print(self.getCLIUsageMessage())
            sys.exit(self._usageExitCode)

        if checkRequired:
            self.validateRequired()

        return args

    def validateRequired(self):
        """
        Checks that all required configuration options have been set.

        :return: True if the validation passes.
        :rtype: bool

        :raises:
            :exc:`.ConfigVarNotDefinedError`
        """
        for varName, isRequired in self._isRequired.items():
            if isRequired and self.__getattribute__(varName) is None:
                raise ConfigVarNotDefinedError(*self._varName2ConfigPath[varName])

    def getCLIUsageMessage(self):
        """
        Return a formatted usage message for the defined CLI.

        :return: The formatted usage message.
        :rtype: str
        """
        return self._cliOptionsSet.getUsageMessage(self.applicationName)
