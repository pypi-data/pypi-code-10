#! /usr/bin/env python

import os
import sys
import argparse
import urlparse
import subprocess


def main(args=sys.argv[1:]):
    """
    Yaghurl: A GitHub URL tool - produce public URLs from local paths.

    Pronounced as if hurling a yag.
    """
    opts = parse_args(args)
    (urlish, relpath, branch, commit) = get_git_info(opts.LOCALPATH, opts.REMOTE)
    (branchurl, commiturl) = calculate_urls(urlish, relpath, branch, commit,
                                            opts.LINE, opts.ENDLINE)

    displayfunc = globals()['display_' + opts.FORMAT]

    with Outputter(opts.OUTPUT) as outfile:
        displayfunc(outfile, opts.MODE, relpath, branch, branchurl,
                    commit, commiturl, opts.LINE, opts.ENDLINE)


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)

    p.add_argument('-m', '--mode',
                   dest='MODE',
                   default='both',
                   choices=['commit', 'branch', 'both'],
                   help='Show a commit or branch specific URL, or show both.')

    p.add_argument('-f', '--format',
                   dest='FORMAT',
                   default='comment',
                   choices=['bare', 'comment'],
                   help=('Display the results in a bare (plain text) or '
                         + 'github-style comment format.'))

    p.add_argument('-o', '--output',
                   dest='OUTPUT',
                   default='both',
                   choices=['stdout', 'xclip', 'both'],
                   help='Write results to stdout or xclip or both.')

    p.add_argument('-r', '--remote',
                   dest='REMOTE',
                   default=None,
                   help=('The remote to link to; if absent pick the first '
                         + 'match from git remote -v'))

    p.add_argument('LOCALPATH',
                   help='Local path within a git repo with a github remote.')

    p.add_argument('LINE',
                   type=int,
                   nargs='?',
                   help='Line number (or starting line).')

    p.add_argument('ENDLINE',
                   type=int,
                   nargs='?',
                   help='Ending line for a range URL.')

    return p.parse_args(args)


def get_git_info(path, remotename):
    path = os.path.abspath(path)
    git = GitWrapper(path)
    urlish = get_remote_urlish(git, remotename)
    branch = git('rev-parse', '--abbrev-ref', 'HEAD').strip()
    commit = git('rev-parse', 'HEAD').strip()
    return (urlish, git.relpath, branch, commit)


def get_remote_urlish(git, remotename):
    for line in git('remote', '-v').splitlines():
        [name, urlish, kind] = line.split()
        if kind == '(fetch)':
            if remotename is None and urlish.find('github.com') != -1:
                return urlish
            elif name == remotename:
                return urlish
        else:
            assert kind == '(push)', 'unknown remote kind: {}'.format(kind)

    assert False, 'remote {} not found.'.format(remotename)


def patch_git_urlish(urlish):
    PREFIX = 'git@github.com:'
    if urlish.startswith(PREFIX):
        guts = urlish[len(PREFIX):]
        return 'https://github.com/' + guts
    else:
        return urlish


class GitWrapper (object):
    def __init__(self, path):
        relparts = []

        def pop_path(d):
            relparts.append(os.path.basename(d))
            return os.path.dirname(d)

        d = pop_path(path)
        while not os.path.isdir(os.path.join(d, '.git')):
            d = pop_path(d)

        self.repodir = d

        relparts.append('.')
        self.relpath = '/'.join(reversed(relparts))

    def __call__(self, *args):
        return subprocess.check_output(['git'] + list(args), cwd=self.repodir)


def calculate_urls(urlish, relpath, branch, commit, line, endline):
    url = patch_git_urlish(urlish)
    urlp = urlparse.urlparse(url)
    urltmpl = '{scheme}://{netloc}/{basepath}/blob/{{}}/{relpath}{linefrag}'.format(
        scheme=urlp.scheme,
        netloc=urlp.netloc,
        basepath=urlp.path,
        relpath=relpath,
        linefrag=calculate_linefrag(line, endline),
        )

    return (urltmpl.format(branch), urltmpl.format(commit))


def calculate_linefrag(line, endline):
    linefrag = ''
    if line is not None:
        linefrag += '#L{}'.format(line)
        if endline is not None:
            linefrag += '-L{}'.format(endline)
    return linefrag


def display_bare(f, mode, _relpath, _branch, branchurl, _commit,
                 commiturl, _line, _endline):

    if mode == 'branch' or mode == 'both':
        f.write('{}\n'.format(branchurl))
    if mode == 'commit' or mode == 'both':
        f.write('{}\n'.format(commiturl))


def display_comment(f, mode, relpath, branch, branchurl, commit,
                    commiturl, line, endline):

    linedesc = calculate_linefrag(line, endline).replace('#', ' ')

    commit = commit[:8]
    if mode == 'both':
        f.write(
            ('[``{relpath}``{linedesc} at ``{commit}``]({commiturl}) '
             + '([latest on branch ``{branch}``]({branchurl}))\n')
            .format(
                relpath=relpath,
                linedesc=linedesc,
                commit=commit,
                commiturl=commiturl,
                branch=branch,
                branchurl=branchurl,
            ))
    elif mode == 'commit':
        f.write(
            '[``{relpath}``{linedesc} at ``{commit}``]({url})\n'
            .format(
                relpath=relpath,
                linedesc=linedesc,
                commit=commit,
                url=commiturl,
            ))
    elif mode == 'branch':
        f.write(
            '[``{relpath}``{linedesc} on branch ``{branch}``]({url})\n'
            .format(
                relpath=relpath,
                linedesc=linedesc,
                branch=branch,
                url=branchurl,
            ))
    else:
        assert False, 'unreachable code'


class Outputter (object):
    def __init__(self, outmode):
        self._files = []
        self._proc = None

        if outmode in ('stdout', 'both'):
            self._files.append(sys.stdout)

        if outmode in ('xclip', 'both'):
            self._proc = subprocess.Popen(
                ['xclip', '-selection', 'clipboard', '-in'],
                stdin=subprocess.PIPE)

            self._files.append(self._proc.stdin)

    # Context interface:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    # File interface:
    def write(self, output):
        for f in self._files:
            f.write(output)

    def close(self):
        for f in self._files:
            f.flush()
            f.close()

        if self._proc is not None:
            self._proc.wait()


if __name__ == '__main__':
    main()
