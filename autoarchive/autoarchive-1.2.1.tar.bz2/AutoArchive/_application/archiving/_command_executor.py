# _command_executor.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2015 Róbert Čerňanský



""":class:`_CommandExecutor` class."""



__all__ = ["_CommandExecutor"]



# {{{ INCLUDES

import shlex

from AutoArchive._infrastructure.ui import VerbosityLevels
from AutoArchive._infrastructure.configuration import Options

# }}} INCLUDES



# {{{ CLASSES

class _CommandExecutor:
    def __init__(self, archiveSpec, externalCommandExecutor, componentUi):
        self.__archiveSpec = archiveSpec
        self.__externalCommandExecutor = externalCommandExecutor
        self.__componentUi = componentUi

        self.__beforeCommand = None
        self.__afterCommand = None
        beforeCommandString = archiveSpec[Options.COMMAND_BEFORE_BACKUP]
        afterCommandString = archiveSpec[Options.COMMAND_AFTER_BACKUP]
        if beforeCommandString is not None:
            self.__beforeCommand = shlex.split(archiveSpec[Options.COMMAND_BEFORE_BACKUP])
        if afterCommandString is not None:
            self.__afterCommand = shlex.split(archiveSpec[Options.COMMAND_AFTER_BACKUP])



    def executeBeforeCommand(self):
        if self.__beforeCommand is not None:
            self.__informVerboseUser(self.__archiveSpec[Options.COMMAND_BEFORE_BACKUP])
            self.__externalCommandExecutor.commandMessage += self.__onCommandMessage
            self.__externalCommandExecutor.execute(self.__beforeCommand[0],
                                                   self.__beforeCommand[1:] if len(self.__beforeCommand) > 1 else None)
            self.__externalCommandExecutor.commandMessage -= self.__onCommandMessage



    def executeAfterCommand(self):
        if self.__afterCommand is not None:
            self.__informVerboseUser(self.__archiveSpec[Options.COMMAND_AFTER_BACKUP])
            self.__externalCommandExecutor.commandMessage += self.__onCommandMessage
            self.__externalCommandExecutor.execute(self.__afterCommand[0],
                                                   self.__afterCommand[1:] if len(self.__afterCommand) > 1 else None)
            self.__externalCommandExecutor.commandMessage -= self.__onCommandMessage



    def __onCommandMessage(self, command, message, isError):
        if isError:
            self.__componentUi.showWarning(message)
        elif self.__componentUi.verbosity != VerbosityLevels.Quiet:
            self.__componentUi.presentLine(message)



    def __informVerboseUser(self, commandString):
        if self.__componentUi.verbosity == VerbosityLevels.Verbose:
            self.__componentUi.showVerbose(str.format("Executing command '{}'", commandString))

# }}} CLASSES
