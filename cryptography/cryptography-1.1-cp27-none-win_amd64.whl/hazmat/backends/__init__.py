# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import absolute_import, division, print_function

import pkg_resources

from cryptography.hazmat.backends.multibackend import MultiBackend


_available_backends_list = None


def _available_backends():
    global _available_backends_list

    if _available_backends_list is None:
        _available_backends_list = [
            # setuptools 11.3 deprecated support for the require parameter to
            # load(), and introduced the new resolve() method instead.
            # This can be removed if/when we can assume setuptools>=11.3. At
            # some point we may wish to add a warning, to push people along,
            # but at present this would result in too many warnings.
            ep.resolve() if hasattr(ep, "resolve") else ep.load(require=False)
            for ep in pkg_resources.iter_entry_points(
                "cryptography.backends"
            )
        ]

    return _available_backends_list

_default_backend = None


def default_backend():
    global _default_backend

    if _default_backend is None:
        _default_backend = MultiBackend(_available_backends())

    return _default_backend
