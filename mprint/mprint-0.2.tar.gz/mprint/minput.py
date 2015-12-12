# Add imput functionalities

# Import mprint
from mprint import mprint, mprintln, colorTable, formatTable

# Fixing raw_input and input problems in Python 3
try:
    input = raw_input
except NameError:
    pass


# Question
def mquestion(text, yes=True):
    yesno = "y/N"
    if yes:
        yesno = "Y/n"

    mprint("%s <bold>[%s]</bold> " % (text, yesno))
    result = input()
    if (result == "" and yes) or (result.lower().startswith("y")):
        return True
    else:
        return False


# Press any key
def mpause(text="Press enter to continue..."):
    mprint(text)
    input()


# Text input
def minput(text=""):
    mprint("<default>%s<bold>" % text)
    result = input()
    mprint("<default>")
    return result


# Function to detect if a variable is a number
def is_number(number=""):
    try:
        float(number)
        return True
    except ValueError:
        return False


# Numeric input
def mnum_input(text="", error="The value is not a number"):
    mprint("<default>%s<bold>" % text)
    result = input()
    mprint("<default>")
    if is_number(result):
        return result
    else:
        mprintln(error, "error")
        return mnum_input(text, error)


# Email input
def memail_input(text="", error="This doesn't look like an email"):
    mprint("<default>%s<bold>" % text)
    result = input()
    mprint("<default>")
    if "@" in result and "." in result:
        return result
    else:
        mprintln(error, "error")
        return memail_input(text, error)
