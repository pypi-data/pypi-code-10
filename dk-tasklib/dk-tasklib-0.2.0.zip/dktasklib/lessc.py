# -*- coding: utf-8 -*-
import os
import sys

from invoke import run, ctask as task

from .package import Package
from .utils import switch_extension, filename, min_name, version_name, join, changed_dir
from .version import add_version, update_template_version

bootstrap = os.path.join(os.environ['SRV'], 'lib', 'bootstrap', 'less')


@task
def version(ctx):
    "Display the lessc version"
    return run("lessc --version")


@task
def lessc(ctx, source, destination="",
          include_path=None,
          strict_imports=False,
          inline_urls=True,
          autoprefix=True,
          cleancss=True
          ):
    if include_path is None:
        include_path = []
    if not destination:
        destination = source[:-len('.less')] + '.css'
    options = ""
    if ctx.verbose:
        options += ' --verbose'
    if include_path:
        options += ' --include-path="%s"' % ';'.join(include_path)
    if strict_imports:
        options += " --strict-imports"
    if inline_urls:
        options += " --inline-urls"
    if autoprefix:
        options += ' --autoprefix="last 4 versions"'
    if cleancss:
        options += ' --clean-css="-b --s0 --advanced"'

    run("lessc {options} {source} {destination}".format(**locals()))


@task
def build_css(ctx, lessfile, dest, version='svn',
              build='build/css', use_bootstrap=True, **kw):
    """Build all .less files into .css.
       `dest` should be the target filename.
    """
    path = kw.pop('path', [])
    if use_bootstrap:
        path.append(bootstrap)

    cssfname = join(build, switch_extension(filename(lessfile), '.css'))
    minfname = min_name(dest)

    # rawcss = join(build, filename(dest))

    if ctx.verbose:
        print >>sys.stderr, 'lessc..'
        
    lessc(
        ctx,
        lessfile,
        minfname,
        include_path=path,
        strict_imports=True,
        inline_urls=True,
        autoprefix=True,
        cleancss=True,
    )
    
    if ctx.verbose:
        print >>sys.stderr, 'verisioning..'
    add_version(ctx, minfname, version_name(minfname), kind=version)


@task(post=[update_template_version])
def build_less(ctx, force=False, verbose=False, src=None, dst=None, **kw):
    """Compile .less to .css  (pakage.json[build_less_input/output]
    """
    if not hasattr(ctx, 'pkg'):
        ctx.pkg = Package()
    if not hasattr(ctx.pkg, 'build_less_input'):
        ctx.pkg.build_less_input = src or 'less/{pkg.name}.less'.format(pkg=ctx.pkg)
    if not hasattr(ctx.pkg, 'build_less_output'):
        ctx.pkg.build_less_output = dst or 'static/{pkg.name}/{pkg.name}.css'.format(pkg=ctx.pkg)
    if not hasattr(ctx, 'force'):
        ctx.force = force
    if not hasattr(ctx, 'verbose'):
        ctx.verbose = verbose
    if ctx.verbose:
        print 'build_less input: ', ctx.pkg.build_less_input
        print 'build_less output:', ctx.pkg.build_less_output

    dirname = os.path.dirname(ctx.pkg.build_less_input)
    with changed_dir(dirname, '**/*.less', force=ctx.force):
        build_css(
            ctx,
            ctx.pkg.build_less_input,
            ctx.pkg.build_less_output,
            version='pkg',
            **kw
        )   
