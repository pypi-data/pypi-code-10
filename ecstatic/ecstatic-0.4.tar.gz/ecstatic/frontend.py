import os

from flask import Blueprint, current_app, abort, send_file

frontend = Blueprint('frontend', __name__)


def serve(fs_path, cfg):
    """Serves an already validated path (i.e. not outside allowed regions)
    to the client."""
    # check if file exists
    if not os.path.exists(fs_path):
        abort(404)

    if os.path.isdir(fs_path):
        if not cfg.getboolean('dirindex', False):
            abort(403, 'Directory listing forbidden.')
        raise NotImplementedError  # TODO: Write easy-on-eyes dirindex

    if not os.path.isfile(fs_path):
        abort(403, 'Not a valid file.')

    # file exists and is valid. server as attachment
    return send_file(fs_path,
                     as_attachment=True,
                     attachment_filename=os.path.basename(fs_path))


def validate_path(root, path):
    base = os.path.realpath(root)
    target = os.path.realpath(os.path.join(base, path))

    # central security check: ensure path does not escape base
    if not os.path.commonprefix([base, target]) == base:
        abort(403, 'Path violates access restrictions.')

    return target


@frontend.route('/', defaults={'path': ''})
@frontend.route('/<path:path>')
def serve_path(path):
    # try to match path
    for regex, fspath, cfg in current_app.exports:
        m = regex.match(path)
        if m:
            break
    else:
        abort(404, 'No export found.')
    match_groups = [v or '' for v in m.groups()]

    new_path = fspath.format(*match_groups)
    root = cfg['root'].format(*match_groups)

    if current_app.debug:
        print('[{}] {!r} -> {} (root: {})'.format(cfg.name, path, new_path,
                                                  root))

    target = validate_path(root, new_path)
    return serve(target, cfg)
