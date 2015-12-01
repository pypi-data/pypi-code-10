from abc import ABCMeta, abstractmethod

from .error import CLIFlagArgumentError, CLIDuplicateOptionException, CLIArgumentTypeError


class CLIOptionsSet(object):
    def __init__(self):
        self._options = {}

    def addOption(self, name, takesArg, helpMsg, varName, type, aliases, flagVal=None):
        if self.hasExistingOption(name):
            raise CLIDuplicateOptionException()

        if takesArg:
            self._options[name] = ArgumentOption(name, helpMsg, varName, type, aliases)
        else:
            self._options[name] = FlagOption(name, helpMsg, varName, type, aliases, flagVal)

        for alias in self._options[name].getAliasOptions():
            if self.hasExistingOption(alias.name):
                raise CLIDuplicateOptionException()

            self._options[alias.name] = alias

    def hasExistingOption(self, name):
        try:
            self._options[name]
            return True
        except KeyError:
            return False

    def getOptionsLists(self, shortOptsAsString=False):
        shortOpts = []
        longOpts = []

        for name, opt in self._options.items():
            if len(name) > 1:
                if opt.takesArgument():
                    name += '='
                longOpts.append(name)
            else:
                if opt.takesArgument():
                    name += ':'
                shortOpts.append(name)

        if shortOptsAsString:
            shortOpts = ''.join(shortOpts)

        return shortOpts, longOpts

    def processOptionInput(self, opt, arg):
        opt = opt.lstrip('-')
        return self._options[opt].processInput(arg)

    def getUsageMessage(self, appName):
        usageStatement = 'usage: ' + appName + ' [options]\n'

        optionStatements = []
        for opt in self._options.values():
            if isinstance(opt, AliasOption):
                continue

            optStrings = []
            opts = [opt.name]
            for alias in opt.getAliasOptions():
                opts.append(alias.name)

            for x in opts:
                optStrings.append('-' + ('-' if len(x) > 1 else '') + x)
                if opt.takesArgument():
                    optStrings[-1] += ' arg'

            optionStatements.append('\t[' + ' | '.join(optStrings) + ']\n\t\t' + opt.getHelpMessage())

        return usageStatement + '\n'.join(optionStatements) + '\n'


class Option(metaclass=ABCMeta):
    def __init__(self, name, helpMsg, varName, type, aliases):
        self.name = name
        self._helpMsg = helpMsg
        self._varName = varName
        self._type = type

        self._aliases = []
        for aliasName in aliases:
            self._aliases.append(AliasOption(aliasName, self))

    @abstractmethod
    def takesArgument(self):
        pass

    def getAliasOptions(self):
        return self._aliases

    @abstractmethod
    def processInput(self, arg):
        pass

    def getHelpMessage(self):
        return self._helpMsg


class ArgumentOption(Option):
    def processInput(self, arg):
        try:
            if self._type == int:
                arg = int(arg)
            elif self._type == float:
                arg = float(arg)
            elif self._type == bool:
                try:
                    arg = int(arg) != 0
                except ValueError:
                    if arg.lower() == 'true':
                        arg = True
                    elif arg.lower() == 'false':
                        arg = False
                    else:
                        raise CLIArgumentTypeError()
        except ValueError:
            raise CLIArgumentTypeError()

        return self._varName, arg

    def takesArgument(self):
        return True


class FlagOption(Option):
    def __init__(self, name, helpMsg, varName, flagType, aliases, flagVal):
        self._assertionValue = flagVal
        super().__init__(name, helpMsg, varName, flagType, aliases)

    def processInput(self, arg):
        if arg:
            raise CLIFlagArgumentError()

        return self._varName, self._assertionValue

    def takesArgument(self):
        return False


class AliasOption(Option):
    def __init__(self, name, option):
        self._option = option
        self.name = name

    def getAliasOptions(self):
        return []

    def processInput(self, arg):
        return self._option.processInput(arg)

    def takesArgument(self):
        return self._option.takesArgument()

    def getHelpMessage(self):
        return self._option.getHelpMessage()