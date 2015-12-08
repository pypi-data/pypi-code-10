class InvalidVersionError(Exception):
    pass

from ._string import String
from .semver import SemVer

classes = [String, SemVer]
schemes = dict((c.__name__.lower(), c) for c in classes)
