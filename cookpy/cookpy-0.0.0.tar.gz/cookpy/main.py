# -*- coding: utf-8 -*-

import os
import subprocess

from . import ninja, arguments, utils


def at_exit():
    try:
        args = arguments.parser.parse_args()
    except SystemExit as e:
        os._exit(int(str(e)))
    else:
        if args.help:
            # This will display the error message.
            utils.enable_stdout()
            arguments.parser.print_help()
        else:
            go()


def go():
    # TODO: Actually clean something.
    if 'clean' in arguments.actions:
        print('Cleaning', os.path.abspath('.'))

    if 'build' in arguments.actions:
        # Save the build description and run it.
        ninja.io.seek(0)

        with open('build.ninja', 'w') as f:
            f.write(ninja.io.read())

        call = ['ninja']
        if arguments.jobs > 0:
            call.extend(['-j', str(arguments.jobs)])
        subprocess.call(call, env=dict(os.environ, NINJA_STATUS='[%p] '))
