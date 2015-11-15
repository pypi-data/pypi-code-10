# This file is part of hgreview.  The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.
'''extension to work with rietveld code review'''

testedwith = '3.2'
buglink = 'https://bitbucket.org/nicoe/hgreview/issues'

import os
import re
import sys
import tempfile
import itertools
import formatter
import htmllib
import urllib
import urllib2
from hashlib import md5

from mercurial.__version__ import version as mercurial_version
from mercurial import hg, extensions, util
from mercurial import patch, mdiff, node, commands

try:
    test = map(int, mercurial_version.split('.')) >= [1, 9]
except ValueError:
    test = True
if test:
    from mercurial.scmutil import revpair, matchfiles
else:
    from mercurial.cmdutil import revpair, matchfiles
try:
    test = map(int, mercurial_version.split('.')) >= [2, 1]
except ValueError:
    test = True
if test:
    from mercurial.copies import mergecopies
else:
    from mercurial.copies import copies as mergecopies


from review import (GetEmail, GetRpcServer, CheckReviewer, MAX_UPLOAD_SIZE,
    EncodeMultipartFormData, UploadSeparatePatches, MercurialVCS,
    DEFAULT_OAUTH2_PORT)


RAW_PATCH_HREF = re.compile('.*/issue[0-9]+_([0-9])+.diff$')


class CodereviewParser(htmllib.HTMLParser):

    def __init__(self):
        self.patch_urls = []
        htmllib.HTMLParser.__init__(self, formatter.NullFormatter())

    def start_a(self, attributes):
        href = dict(attributes).get('href', '')
        match = RAW_PATCH_HREF.match(href)
        if not match:
            return
        else:
            patch_num = int(match.groups()[0])
        self.patch_urls.append((patch_num, href))
        self.patch_urls.sort(reverse=True)

    @property
    def patch_url(self):
        if not self.patch_urls:
            return None
        return self.patch_urls[0][1]


def _get_issue_file(repo):
    return os.path.join(repo.root, '.hg', 'review_id')


def _get_issue_id(repo):
    issue_file = _get_issue_file(repo)
    if os.path.isfile(issue_file):
        return open(issue_file, 'r').read().strip()


def _get_server(ui):
    return ui.config('review', 'server',
        default='http://codereview.appspot.com')


def _get_base_url(ui):
    return ui.config('review', 'base_url', default=None)


def _get_oauth2(ui):
    return ui.configbool('review', 'oauth2', default=False)


def _get_oauth2_port(ui):
    return ui.configint('review', 'oauth2_port', default=DEFAULT_OAUTH2_PORT)


def _get_oauth2_webbrowser(ui):
    return ui.configbool('review', 'oauth2_webbrowser', default=True)


def _get_oauth2_args(ui):
    return dict(
        use_oauth2=_get_oauth2(ui),
        oauth2_port=_get_oauth2_port(ui),
        open_oauth2_local_webbrowser=_get_oauth2_webbrowser(ui),
        )


def get_vcs(opts, root):

    class FakeOptions(object):
        download_base = False
        revision = opts['rev']
        num_upload_threads = 8
        # Fix "local variable 'result' referenced before assignment"
        # in UploadFile
        verbose = True
        email = None

    return MercurialVCS(FakeOptions(), root)


def nested_diff(ui, repo, opts=None):
    for npath in repo.nested:
        if npath == '.':
            nrepo = repo
        else:
            lpath = os.path.join(repo.root, npath)
            lui = ui.copy()
            lui.readconfig(os.path.join(lpath, '.hg', 'hgrc'))
            nrepo = hg.repository(lui, lpath)
        node1, node2 = revpair(nrepo, [])
        yield patch.diff(nrepo, node1, node2, opts=mdiff.diffopts(git=True),
            prefix=(npath if npath != '.' else ''))


def nested_status(ui, repo):
    status = {}
    for npath in repo.nested:
        if npath == '.':
            nrepo = repo
        else:
            lpath = os.path.join(repo.root, npath)
            lui = ui.copy()
            lui.readconfig(os.path.join(lpath, '.hg', 'hgrc'))
            nrepo = hg.repository(lui, lpath)
        node1, node2 = revpair(nrepo, [])
        status[nrepo] = dict(zip(
            ('modified', 'added', 'removed', 'deleted', 'unknown', 'ignored',
                'clean'),
            nrepo.status(node1, node2, unknown=True)))
    return status


def add_nested_info(root_repo, status):
    root_path = root_repo.root
    for nrepo, repo_status in status.items():
        common = len(os.path.commonprefix([root_path, nrepo.root]))
        status[nrepo]['prefix'] = nrepo.root[common + 1:]


def review(ui, repo, *args, **opts):
    """
    Upload patch to a rietveld website, create a new issue and remember its ID
    """
    issue_file = _get_issue_file(repo)
    if opts.get('clean'):
        os.unlink(issue_file)
        return

    revs = [opts['rev']] if opts.get('rev') else []
    node1, node2 = revpair(repo, revs)
    modified, added, removed, deleted, unknown, ignored, clean = \
            repo.status(node1, node2, unknown=True)

    server = _get_server(ui)
    if opts.get('id') or opts.get('url'):
        issue_id = _get_issue_id(repo) or ''
        msg = '%s' % issue_id
        if opts.get('url'):
            msg = '%s/%s/' % (server, msg)
        ui.status(msg, '\n')
        return

    username = ui.config('review', 'username')
    if not username:
        username = GetEmail('Email (login for uploading to %s)' % server)
        ui.setconfig('review', 'username', username)
    host_header = ui.config('review', 'host_header')
    account_type = ui.config('review', 'account_type', 'GOOGLE')
    rpc_server = GetRpcServer(server, username, host_header, True,
        account_type, **_get_oauth2_args(ui))

    base_url = _get_base_url(ui)

    if opts.get('fetch'):
        if modified or added or removed or deleted:
            ui.warn('The repository is not clean.', '\n')
            sys.exit(1)
        if not opts.get('issue'):
            issue_id = _get_issue_id(repo)
            if not issue_id:
                ui.status('No .hg/review_id found', '\n')
                return
        else:
            issue_id = opts.get('issue')
        msg = 'Looking after issue %s/%s patch' % (server, issue_id)
        ui.status(msg, '\n')
        cp = CodereviewParser()
        try:
            html = rpc_server.Send('/%s' % issue_id)
        except urllib2.HTTPError as e:
            ui.status('Unable to fetch the patch: {}'.format(e), '\n')
            return
        cp.feed(html)

        if not cp.patch_url:
            ui.status('No raw patch URL found', '\n')
            return
        with tempfile.NamedTemporaryFile(
                delete=not opts.get('keep')) as patch_fd:
            patch_fd.write(rpc_server.Send(cp.patch_url))
            patch_fd.flush()
            commands.import_(ui, repo, patch_fd.name, no_commit=True, base='',
                strip=1, prefix='')
            if os.path.isfile(issue_file):
                ui.status('.hg/review_id already exists: not overriding it',
                    '\n')
            else:
                open(issue_file, 'w').write(issue_id)
        return

    is_nested = (
        (opts.get('nested')
            or ui.config('review', 'nested', default=False))
        and 'hgnested' in extensions.enabled()
        and len(repo.nested) > 1)
    revs = [opts['rev']] if opts.get('rev') else []
    if is_nested:
        if revs:
            raise util.Abort('Specifying a revision on a nested repo has no sense')
        status = nested_status(ui, repo)
    else:
        status = {}
        n1, n2 = revpair(repo, revs)
        status[repo] = dict(zip(
                ('modified', 'added', 'removed', 'deleted', 'unknown',
                    'ignored', 'clean'),
                repo.status(n1, n2, unknown=True)))
    add_nested_info(repo, status)

    if any(repo_status.get('unknown') for repo_status in status.values()):
        ui.status('The following files are not added to version control:',
            '\n\n')
        for repo_status in status.values():
            for fname in repo_status['unknown']:
                if repo_status['prefix']:
                    fname = os.path.join(repo_status['prefix'], fname)
                ui.status(fname, '\n')
        cont = ui.prompt("\nAre you sure to continue? (y/N) ", 'N')
        if cont.lower() not in ('y', 'yes'):
            sys.exit(0)

    opts['git'] = True
    if not is_nested:
        difffiles = patch.diff(repo, n1, n2, opts=mdiff.diffopts(git=True))
    else:
        difffiles = itertools.chain.from_iterable(nested_diff(ui, repo,
                opts=mdiff.diffopts(git=True)))

    svndiff, filecount = [], 0
    for diffedfile in difffiles:
        for line in diffedfile.split('\n'):
            m = re.match(patch.gitre, line)
            if m:
                # Modify line to make it look like as it comes from svn diff.
                # With this modification no changes on the server side are
                # required to make upload.py work with Mercurial repos.
                # NOTE: for proper handling of moved/copied files, we have to
                # use the second filename.
                filename = m.group(2)
                svndiff.append("Index: %s" % filename)
                svndiff.append("=" * 67)
                filecount += 1
            else:
                svndiff.append(line)
    if not filecount:
        # No valid patches in hg diff
        sys.exit(1)
    data = '\n'.join(svndiff) + '\n'
    files = {}

    for nrepo, repo_status in status.items():
        n1, n2 = revpair(nrepo, revs)
        base_rev = nrepo[n1]
        current_rev = nrepo[n2]
        null_rev = nrepo[node.nullid]

        # getting informations about copied/moved files
        copymove_info = mergecopies(nrepo, base_rev, current_rev, null_rev)[0]
        for newname, oldname in copymove_info.items():
            oldcontent = base_rev[oldname].data()
            newcontent = current_rev[newname].data()
            is_binary = "\0" in oldcontent or "\0" in newcontent
            if repo_status['prefix']:
                newname = os.path.join(repo_status['prefix'], newname)
            files[newname] = (oldcontent, newcontent, is_binary, 'M')

        # modified files
        for filename in matchfiles(nrepo, repo_status['modified']):
            oldcontent = base_rev[filename].data()
            newcontent = current_rev[filename].data()
            is_binary = "\0" in oldcontent or "\0" in newcontent
            if repo_status['prefix']:
                filename = os.path.join(repo_status['prefix'], filename)
            files[filename] = (oldcontent, newcontent, is_binary, 'M')

        # added files
        for filename in matchfiles(repo, repo_status['added']):
            oldcontent = ''
            newcontent = current_rev[filename].data()
            is_binary = "\0" in newcontent
            if repo_status['prefix']:
                filename = os.path.join(repo_status['prefix'], filename)
            files[filename] = (oldcontent, newcontent, is_binary, 'A')

        # removed files
        for filename in matchfiles(repo, repo_status['removed']):
            if filename in copymove_info.values():
                # file has been moved or copied
                continue
            oldcontent = base_rev[filename].data()
            newcontent = ''
            is_binary = "\0" in oldcontent
            if repo_status['prefix']:
                filename = os.path.join(repo_status['prefix'], filename)
            files[filename] = (oldcontent, newcontent, is_binary, 'R')

    if not server:
        raise util.Abort('No server defined')
    ui.status('Server used %s' % server, '\n')

    form_fields = []

    message = ''
    issue_id = _get_issue_id(repo) or opts.get('issue')
    if issue_id:
        if not os.path.isfile(issue_file):
            open(issue_file, 'w').write(issue_id)
            ui.status('Creating %s file' % issue_file, '\n')
        prompt = "Message describing this patch set:"
        if opts.get('message'):
            message = opts['message']
        else:
            message = ui.prompt(prompt, '')
        if not message:
            raise util.Abort('Empty message')

        form_fields.append(('subject', message))
    else:
        if opts.get('message'):
            desc = opts['message']
        else:
            text = []
            text.append('')
            text.append('')  # Empty line between message and comments
            text.append('HG: Enter review description. '
                'Lines beginning with "HG:" are removed.')
            text.append('HG: The first line will be the subject '
                'and the others the description')
            text.append('HG: --')
            text.append('HG: user: %s' % username)
            text.append('HG: server: %s' % server)
            desc = ui.edit('\n'.join(text), ui.username)
            desc = re.sub('(?m)^HG:.*(\n|$)', '', desc)
            if not desc.strip():
                raise util.Abort('Empty review description')
        desc = desc.splitlines()
        subject = desc[0]
        if not subject:
            raise util.Abort('Empty review subject')
        desc = desc[1:]
        form_fields.append(('subject', subject))
        form_fields.append(('description', '\n'.join(desc)))

    repo_guid = repo[0].hex()
    if not base_url and repo_guid:
        form_fields.append(('repo_guid', repo_guid))
    if base_url:
        form_fields.append(('base', base_url))
    if issue_id:
        form_fields.append(('issue', issue_id))
    if username:
        form_fields.append(('user', username))
    if opts.get('reviewers'):
        for reviewer in opts['reviewers']:
            CheckReviewer(reviewer)
        form_fields.append(('reviewers', ','.join(opts['reviewers'])))
    cc_header = ui.config('review', 'cc_header')
    if cc_header:
        for cc in cc_header.split(','):
            CheckReviewer(cc)
        form_fields.append(("cc", cc_header))

    # Send a hash of all the base file so the server can determine if a copy
    # already exists in an earlier patchset.
    base_hashes = []
    for filename, info in files.iteritems():
        if info[0] is not None:
            checksum = md5(info[0]).hexdigest()
            base_hashes.append('%s:%s' % (checksum, filename))
    form_fields.append(('base_hashes', '|'.join(base_hashes)))

    # I choose to upload content by default see upload.py for other options
    form_fields.append(('content_upload', '1'))
    if len(data) > MAX_UPLOAD_SIZE:
        uploaded_diff_file = []
        form_fields.append(('separate_patches', '1'))
    else:
        uploaded_diff_file = [('data', 'data.diff', data)]
    ctype, body = EncodeMultipartFormData(form_fields, uploaded_diff_file)
    response_body = rpc_server.Send('/upload', body, content_type=ctype)

    lines = response_body.splitlines()
    patchset = None
    if len(lines) > 1:
        msg = lines[0]
        patchset = lines[1].strip()
        patches = [x.split(' ', 1) for x in lines[2:]]
    else:
        msg = response_body
    ui.status(msg, '\n')
    if not (response_body.startswith('Issue created.')
            or response_body.startswith('Issue updated.')):
        sys.exit(0)
    issue_id = msg[msg.rfind('/') + 1:]
    open(issue_file, 'w').write(issue_id)

    vcs = get_vcs(opts, repo.root)
    if not uploaded_diff_file:
        patches = UploadSeparatePatches(issue_id, rpc_server, patchset, data,
            vcs.options)
    vcs.UploadBaseFiles(issue_id, rpc_server, patches, patchset, vcs.options,
        files)

    payload = {}
    if (opts.get('send_email')
            or ui.configbool('review', 'send_email')
            or opts.get('send_patch')
            or ui.configbool('review', 'send_patch')):
        payload['send_mail'] = 'yes'
        if opts.get('send_patch') or ui.configbool('review', 'send_patch'):
            payload['attach_patch'] = 'yes'
    if message:
        payload['message'] = message
    payload = urllib.urlencode(payload)
    rpc_server.Send('/%s/upload_complete/%s' % (issue_id,
            patchset if patchset else ''),
        payload=payload)

# Add option for description, private
cmdtable = {
    'review': (review, [
        ('c', 'clean', False, 'Remove review info'),
        ('i', 'issue', '', 'Issue number. Defaults to new issue'),
        ('m', 'message', '', 'Codereview message'),
        ('n', 'nested', False, 'Use nested diff'),
        ('r', 'reviewers', [], 'Add reviewers'),
        ('', 'rev', '', 'Revision number to diff against'),
        ('', 'send_email', None, 'Send notification email to reviewers'),
        ('', 'send_patch', None, 'Same as send_email but include diff as an '
            "attachment, and prepend email subject with 'PATCH:'"),
        ('', 'id', None, 'ouput issue id'),
        ('', 'url', None, 'ouput issue URL'),
        ('', 'fetch', None, 'Fetch patch and apply to repository'),
        ('', 'keep', False, 'Keep patch file after application'),
    ], "hg review [options]"),
}


def review_commit(orig, ui, repo, *pats, **opts):
    issue_id = _get_issue_id(repo)
    issue_file = _get_issue_file(repo)
    has_issuefile = os.path.isfile(issue_file)

    if has_issuefile:
        opts['extramsg'] = 'Review ID: %s' % issue_id
    orig(ui, repo, *pats, **opts)

    if has_issuefile:
        server = _get_server(ui)
        username = ui.config('review', 'username')
        if server and not username:
            username = GetEmail('Email (login for uploading to %s)' % server)
        if server and username:
            host_header = ui.config('review', 'host_header')
            account_type = ui.config('review', 'account_type', 'GOOGLE')
            rpc_server = GetRpcServer(server, username, host_header, True,
                account_type, **_get_oauth2_args(ui))
            rpc_server.Send('/%s/close' % issue_id)
        os.unlink(issue_file)


def uisetup(ui):
    extensions.wrapcommand(commands.table, 'commit', review_commit)
