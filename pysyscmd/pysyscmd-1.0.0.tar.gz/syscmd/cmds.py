# -*- coding: utf-8 -*-

class Syscmd(object):
    def _cmd(self, cmd, *args, **kwargs):
        """Execute system commands

        Args:
            *args: The positional arguments are used as arguments to the
            command. For example, the following python code:

                _cmd("git, "commit", "--help")

            would execute:

                git commit --help

            f: One of CALL, CHECK_CALL, or CHECK_OUTPUT. Corresponds to the
            function from the subprocess module called to execute the command.
            Defaults to CHECK_CALL

            **kwargs: The keyword arguments are passed through to the subprocess
            function as-is.

        Returns:
            Whatever is returned by the respective subprocess function. For
            example, f=CALL would return the returncode attribute, and
            f=CHECK_OUTPUT would return the content of stdout.

        Exmples:
            The following call:

                _cmd("git", "commit", "-m", "Commit Message", cwd="/path/to/repo")

            results in:

                subprocess.check_call(["git", "commit", "-m", "Commit Message"], cwd="/path/to/repo")

            And:

                _cmd("git", "checkout", "-b", "branch_name", f=CHECK_OUTPUT, cwd="/path/to/repo")

            results in:

                subprocess.check_output(["git", "checkout", "-b", "branch_name"], cwd="/path/to/repo")
        """

        import syscmd

        f = kwargs.pop('f', syscmd.CHECK_CALL)
        f = syscmd._sub_calls[f]

        full_args = (cmd,) + tuple(args)

        full_kwargs = syscmd._default_subprocess_kwargs.copy()
        full_kwargs.update(kwargs)

        return f(full_args, **full_kwargs)


    def _which(self, cmd):
        import os
        for path in os.environ.get('PATH', '').split(os.pathsep):
            if path == "":
                continue

            full_path = os.path.join(path, cmd)

            if os.access(full_path, os.X_OK):
                return full_path

        return None

    def __getattr__(self, name):
        from functools import partial
        cmd = self._which(name)

        if cmd != None:
            return partial(self._cmd, cmd)

        raise AttributeError("'module' object has no attribute %r" % (name,))

import sys
sys.modules[__name__] = Syscmd()
