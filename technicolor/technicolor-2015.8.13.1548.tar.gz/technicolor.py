################################################################################
#                                                                              #
# technicolor                                                                  #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides color logging in Python.                               #
#                                                                              #
# copyright (C) 2014 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for    #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

name    = "technicolor"
version = "2015-08-13T1548Z"

import ctypes
import logging
import os
import inspect
import functools
 
class ColorisingStreamHandler(logging.StreamHandler):

    # color names to indices
    colorMap = {
        'black':   0,
        'red':     1,
        'green':   2,
        'yellow':  3,
        'blue':    4,
        'magenta': 5,
        'cyan':    6,
        'white':   7,
    }

    # level colour specifications
    # syntax: logging.level: (background color, foreground color, bold)
    levelMap = {
        logging.DEBUG:    (None,   'blue',    False),
        logging.INFO:     (None,   'white',   False),
        logging.WARNING:  (None,   'yellow',  False),
        logging.ERROR:    (None,   'red',     False),
        logging.CRITICAL: ('red',  'white',   True),
    }

    # control sequence introducer
    CSI = '\x1b['

    # normal colours
    reset = '\x1b[0m'
 
    def istty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()
 
    def emit(self, record):
        try:
            message = self.format(record)
            stream  = self.stream
            if not self.istty:
                stream.write(message)
            else:
                self.outputColorised(message)
            stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
 
    def outputColorised(self, message):
        self.stream.write(message)
 
    def colorise(self, message, record):
        if record.levelno in self.levelMap:
            backgroundColor, \
            foregroundColor, \
            bold = self.levelMap[record.levelno]
            parameters = []
            if backgroundColor in self.colorMap:
                parameters.append(str(self.colorMap[backgroundColor] + 40))
            if foregroundColor in self.colorMap:
                parameters.append(str(self.colorMap[foregroundColor] + 30))
            if bold:
                parameters.append('1')
            if parameters:
                message = ''.join((
                    self.CSI,
                    ';'.join(parameters),
                    'm',
                    message,
                    self.reset
                ))
        return message
 
    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        if self.istty:
            # Do not colorise traceback.
            parts    = message.split('\n', 1)
            parts[0] = self.colorise(parts[0], record)
            message  = '\n'.join(parts)
        return(message)

def log(function):

    @functools.wraps(function)
    def decoration(
        *args,
        **kwargs
        ):
        # Get the names of all of the function arguments.
        arguments = inspect.getcallargs(function, *args, **kwargs)
        logging.debug(
            "function '{functionName}' called by '{callerName}' with arguments:"
            "\n{arguments}".format(
                functionName = function.__name__,
                callerName   = inspect.stack()[1][3],
                arguments    = arguments
            ))
        result = function(*args, **kwargs)
        logging.debug("function '{functionName}' result: {result}\n".format(
            functionName = function.__name__,
            result       = result
        ))

    return(decoration)
