class VersionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self._msg = msg

    @property
    def msg(self):
        return self._msg
