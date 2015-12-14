# -*- coding: utf-8 -*-

from invoke import ctask as task


@task
def is_installed(ctx, pkgname, version=None):
    "Check if an npm package is installed."
    rc = ctx.run('npm ls -g --depth=0 {pkgname} >NUL'.format(**locals())).return_code
    ctx[pkgname] = rc == 0


@task
def isinstalled(ctx, pkgname):
    "Check if an npm package is installed."
    rc = ctx.run('which {pkgname}'.format(**locals()), hide=True).return_code
    ctx[pkgname] = rc == 0


