#!/usr/bin/env python
import sys
import os

BASHCOMPLETE_CONFIG = '''#-*- mode: shell-script;-*-
# Debian GNU/Linux python completion

_python()
{
    pybash=`pybashcomplete $COMP_LINE`
    if [[ $pybash =~ COMPLETE:(.+) ]] ; then
        COMPREPLY="${BASH_REMATCH[1]}"
    elif [[ $pybash =~ MULTIPLE:(.+) ]] ; then
        COMPREPLY=(${BASH_REMATCH[1]})
    fi
}
'''


def main():

    if os.path.isdir('/etc/bash_completion.d'):
        try:
            with open('/etc/bash_completion.d/pybashcomplete', 'w') as f:
                f.write(BASHCOMPLETE_CONFIG)
        except Exception:
            import traceback
            traceback.print_exc()
            sys.stderr.write('Exception occurred on installation.\n'
                             'You need to install with sudo or root.\n')
    else:
        sys.stderr.write('/etc/bash_completion.d directory not found.\n'
                         'Installation failed. If your environment places bash '
                         'completion scripts in a different area, paste this '
                         'script there: \n' + BASHCOMPLETE_CONFIG)
