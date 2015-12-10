class VersionError(Exception):
    VERSION_UNMATCHED = 1
    DIRTY             = 2
    NO_GIT            = 3
    NO_TAGS           = 4
    NOT_AT_TAG        = 5

    def __init__(self, msg, errno=None):
        super().__init__(msg)
        self._msg   = msg
        self._errno = errno

    @property
    def msg(self):
        return self._msg

    @property
    def errno(self):
        return self._errno
