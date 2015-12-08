import re

from . import InvalidVersionError
from .base import BaseScheme

class SemVer(BaseScheme):
    """
    http://semver.org/spec/v2.0.0.html
    """

    def __init__(self, s):
        if not re.match('[^\.]+\.[^\.]+\..+', s):
            raise InvalidVersionError('Format must be MAJOR.MINOR.PATCH, not "%s"' % s)

        major, minor, patch = s.split('.', 2)

        if not re.match('(0|[1-9]\d*)$', major):
            raise InvalidVersionError('MAJOR version must be a non-negative integer, and must not contain leading zeros - "%s"' % major)
        major = int(major)

        if not re.match('(0|[1-9]\d*)$', minor):
            raise InvalidVersionError('MINOR version must be a non-negative integer, and must not contain leading zeros - "%s"' % minor)
        minor = int(minor)

        patch = self.PatchVersion(patch)

        super(SemVer, self).__init__((major, minor, patch), s)


    class PatchVersion(BaseScheme):
        def __init__(self, s):
            """
            Helps to sort patch versions like "0-alpha+001"
            """
            match = re.match('(\d*)(.*)', s)
            if not match:
                raise InvalidVersionError('PATCH version must begin with a digit - "%s"' % s)
            version = match.group(1)
            extra = match.group(2)

            if not re.match('(0|[1-9]\d*)$', version):
                raise InvalidVersionError('PATCH version must begin with a non-negative integer, and must not contain leading zeros - "%s"' % s)
            version = int(version)

            match = re.match('(.*)\+(.*)', extra)
            if match:
                prerelease = match.group(1)
                build = match.group(2)
                if not re.match('[0-9A-Za-z-]+', build):
                    raise InvalidVersionError('Build metadata in PATCH version improperly formatted - "%s"' % build)
                # throw away build info
            else:
                prerelease = extra

            if prerelease:
                if prerelease.startswith('.'):
                    raise InvalidVersionError('Four top-level version identifiers are not allowed - required format is MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]')
                if not prerelease.startswith('-'):
                    raise RuntimeError('Something went wrong when parsing "%s" - prerelease version should start with a "-"' % s)
                sort_order = (version, 0, SemVer.PrereleaseVersion(prerelease[1:]))
            else:
                sort_order = (version, 1)

            super(SemVer.PatchVersion, self).__init__(sort_order)

    class PrereleaseVersion(BaseScheme):
        def __init__(self, s):
            """
            Helps to sort prerelease versions like "x.7.z.92"
            """
            values = ()
            for identifier in s.split('.'):
                if not re.match('[0-9A-Za-z-]+', identifier):
                    raise InvalidVersionError('Invalid identifier "%s" in prerelease section of PATCH version' % identifier)
                if re.match('\d+$', identifier):
                    if not re.match('(0|[1-9]\d*)$', identifier):
                        raise InvalidVersionError('Numeric identifiers in prerelease version must not contain leading zeros - "%s"' % identifier)
                    # sort numerically (lower than strings)
                    values += (1, int(identifier))
                else:
                    # sort lexically (higher than numbers)
                    values += (2, identifier)

            super(SemVer.PrereleaseVersion, self).__init__(values)

