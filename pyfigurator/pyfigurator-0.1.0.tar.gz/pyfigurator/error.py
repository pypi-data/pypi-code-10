__all__ = ['PyfiguratorError', 'ConfigSchemaError', 'ConfigVarNotDefinedError', 'CLISchemaError', 'CLIFlagArgumentError',
           'ConfigValueError', 'ConfigFileNotFoundError', 'CLIDuplicateOptionException', 'CLIArgumentTypeError']


class PyfiguratorError(Exception):
    """
    All Exceptions raised by pyfigurator are subclasses of this.

    *If a non-subclassed PyfiguratorError is raised, this is unexpected behavior.  Please file a bug report.*

    The only exception to the above rule is when :meth:`.Config.parseCommandLineArgs` prints a usage statement and raises
    :exc:`SystemExit`.
    """
    def __init__(self, msg='General Pyfigurator Library Error'):
        super().__init__(msg)


class ConfigSchemaError(PyfiguratorError):
    """
    Raised when the Config Schema is invalid.
    """
    def __init__(self):
        super().__init__('The provided config schema is invalid.')


class ConfigFileNotFoundError(PyfiguratorError):
    """
    Raised when the config file at the given path cannot be opened during :meth:`.Config.parseConfigFile`.
    """
    def __init__(self):
        super().__init__('Error reading the given config file.')


class ConfigVarNotDefinedError(PyfiguratorError):
    """
    Raised when a required config variable is not defined.
    """
    def __init__(self, section, variable):
        super().__init__('There is no value provided for "' + variable + '" in section "' + section + '".')


class CLISchemaError(PyfiguratorError):
    """
    Raised when the CLI Schema is invalid.
    """
    def __init__(self):
        super().__init__('The provided CLI schema is invalid')


class CLIDuplicateOptionException(CLISchemaError):
    """
    Raised when the CLI Schema specifies two options with the same name or alias.
    """


class CLIFlagArgumentError(PyfiguratorError):
    """
    Raised if an argument is given for a flag option.
    """
    def __init__(self):
        super().__init__('An argument exists for a non-argument option.')


class CLIArgumentTypeError(PyfiguratorError):
    """
    Raised if an argument is given for a flag option.
    """
    def __init__(self):
        super().__init__('The given argument cannot translate to the correct type.')


class ConfigValueError(PyfiguratorError):
    """
    Raised if a value is given that doesn't match the expected type of the configuration variable.
    """
    def __init__(self):
        super().__init__('Invalid Value for configuration.')
