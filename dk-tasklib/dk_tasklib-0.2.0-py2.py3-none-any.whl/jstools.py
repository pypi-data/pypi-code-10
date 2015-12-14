# -*- coding: utf-8 -*-

from invoke import run, ctask as task
import sys


@task
def browserify(ctx, source, dest, require=(), external=(), entry=None):
    """
    Run ``browserify``

    Args:
        ctx:        context
        source:     root source file
        dest:       path/name of assembled file
        require:
        external:
        entry:

    Returns:

    """
    options = ""
    for r in require:
        options += ' -r "%s"' % r
    for e in external:
        options += ' -x "%s"' % e
    if entry:
        options += ' -e "%s"' % entry
    cmd = "browserify {source} -o {dest} {options}".format(**locals())
    if ctx.verbose:
        print >> sys.stderr, cmd
    run(cmd)
