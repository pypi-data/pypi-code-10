import os
import os.path as osp
import shutil


import vcr as _vcr

__all__ = ['vcr', 'merge_dir']

CASSETTE_LIBRARY_DIR = osp.join(osp.dirname(__file__), 'fixtures/cassettes')


def cleanup_quay_http_response(request):
    """Prevent some response headers to be record in cassettes"""
    request.get('headers', {}).pop('set-cookie', None)
    return request


#: instance of :py:class:`vcr.VCR` to be used by all unit-tests
vcr = _vcr.VCR(
    cassette_library_dir=CASSETTE_LIBRARY_DIR,
    record_mode='once',
    path_transformer=_vcr.VCR.ensure_suffix('.yaml'),
    filter_headers=['authorization', 'Cookie'],
    before_record_response=cleanup_quay_http_response
)


def merge_dir(src, dest, force=False):
    """ Merge content of a directory to another

    :param basestring src:
      path to directory whose content has to be copied.

    :param basestring dest:
      path to the destination directory

    :param bool force:
      wheter existing files in `dest` are overwriten or not.
    """
    for root, dirs, files in os.walk(src):
        for d in dirs:
            dest_dir = osp.join(dest, osp.join(root[len(src) + 1:], d))
            if not osp.isdir(dest_dir):
                os.makedirs(dest_dir)
        for f in files:
            dest_file = osp.join(dest, osp.join(root[len(src) + 1:], f))
            if force or not osp.isfile(dest_file):
                shutil.copy(osp.join(root, f), dest_file)
