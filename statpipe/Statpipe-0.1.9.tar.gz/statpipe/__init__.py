import __future__
import json
import os
import subprocess
from hashlib import sha1

DEFAULT_STATA_EXECUTABLE = "/Applications/Stata/Stata.app/Contents/MacOS/Stata"


def get_prefs():
    statrc = os.path.expanduser('.statrc')

    try:
        prefs = json.loads(open(statrc).read())
    except IOError:
        print("No config file found, writing defaults to %s\n" % (statrc,))
        prefs = {
            'STATA_EXECUTABLE': DEFAULT_STATA_EXECUTABLE
        }
        open(statrc, "w").write(json.dumps(prefs))

    # complain if we can't find Stata itself
    if not os.path.isfile(prefs['STATA_EXECUTABLE']):
        raise Exception("Stata executable not found at {}. Try editing ~/.statrc to tell me where it is.".format(prefs['STATA_EXECUTABLE']))

    return prefs


def run_stata_code(code, quiet=True):
    # save the temporary files under a hash of the code so we can cache things
    codehash = sha1(code.encode()).hexdigest()
    tmpdo = "{}.do".format(codehash)
    tmplog = "{}.log".format(codehash)

    prefs = get_prefs()

    output = ""
    if (not os.path.exists(tmplog)):
        if not quiet:
            output += "Running code now\n"

        with open(tmpdo, 'w') as f:
            f.write(code + "\n")
        result = subprocess.check_output([prefs['STATA_EXECUTABLE'], "-q", "-b", "-e", "do", tmpdo])
    else:
        if not quiet:
            output += "Cached output re-used\n"

    with open(tmplog, 'r') as f:
        # delete some crufty extra space
        output += "".join(f.readlines()[2:-3])

    return output


