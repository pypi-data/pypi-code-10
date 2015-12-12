# MPrint - Markup Print
# Is a CLI text output that uses XML tags to print markup formatted results
# Developed by Artur 'h0m3' Paiva
# Under the MIT Licese
#

# Import future print to Python 2.7 compatbility
from __future__ import print_function

# Imports colorama for Windows based ASCII output
try:
    import colorama
    colorama.init()
except ImportError as exception:
    from sys import platform
    if platform.startswith("win"):
        raise exception

# ASCII Color Table
colorTable = {
        "black": 0,
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
        "default": 9,
        "error": 1,
        "warning": 3,
        "info": 4
    }

# ASCII Format Table
formatTable = {
        "normal": 0,
        "bold": 1,
        "italic": 3,
        "underscore": 4,
        "blink": 5,
        "negative": 6,
        "b": 1,
        "i": 3,
        "u": 4
    }


# Export markup text to ASCII characters for language
def markup(string):
    colorStack = [9]
    bgcolorStack = [9]
    formatStack = [0]

    while '<' in string and '>' in string:
        newString = string.split("<", 1)[0]
        tags = string.split('<', 1)[1].split('>', 1)[0].split()
        if tags[0][0] == '/':
            tags[0] = tags[0][1:]
            if tags[0] == 'color' and len(colorStack) > 1:
                colorStack.pop()
            elif tags[0] == 'bgcolor' and len(bgcolorStack) > 1:
                bgcolorStack.pop()
            elif len(formatStack) > 1:
                formatStack.reverse()
                formatStack.remove(formatTable[tags[0]])
                newString += "\033[0m"
                for item in formatStack:
                    newString += "\033[%dm" % item
                formatStack.reverse()
        else:
            try:
                if tags[0] == 'br':
                    newString += "\n"
                elif tags[0] == "tab":
                    newString += "\t"
                if tags[0] == 'color':
                    if len(tags) is 1:
                        tags[1] = "default"
                    colorStack.append(colorTable[tags[1]])
                elif tags[0] == 'bgcolor':
                    if len(tags) is 1:
                        tags[1] = "default"
                    bgcolorStack.append(colorTable[tags[1]])
                else:
                    if tags[0] in formatTable:
                        formatStack.append(formatTable[tags[0]])
            except:
                raise SyntaxError("Invalid argument: %s" % tags[1])
        newString += "\033[%d;%d;%dm" % (
                                    formatStack[-1],
                                    colorStack[-1]+30,
                                    bgcolorStack[-1]+40
                                    )
        newString += string.split(">", 1)[1]
        string = newString
    return string


# Print markup characters to screen
def mprint(string, color="default", symbol=""):
    if symbol != "":
        symbol = "<bold>%s</bold> " % symbol
    print(markup("<color %s>%s%s</color>" % (color, symbol, string)), end="")


# Same as 'mprint' but add a new line at the end
def mprintln(string=None, color="default", symbol=""):
    if string is None:
        print()
    else:
        mprint(string, color, symbol)
        print()


# Clear the screen
def mclear(bgcolor="default"):
    print("\033[%sm\033[2J" % str(colorTable[bgcolor]+40), end="")


# Reset the color attributes
def mreset():
    print('\033[0m', end="")
