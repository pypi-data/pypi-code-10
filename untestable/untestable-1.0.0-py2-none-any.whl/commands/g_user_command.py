import json
from untestable.commands.command import Command


class GUserCommand(Command):
    """
    Use the BitBucket client to get details of a user.
    """

    NAME = "g-user"

    def __init__(self, io, creds_flow, bbclient):
        self._io = io
        self._creds_flow = creds_flow
        self._bbclient = bbclient
        return

    def can_handle(self, command):
        return command == self.NAME

    def name(self):
        return self.NAME

    def run(self):
        creds = self._creds_flow.run()

        response = self._bbclient.get_user(creds)

        if response.status_code == 200:
            del response.body["repositories"]
            self._io.display((json.dumps(response.body,
                                         indent=4,
                                         separators=(",", ":"),
                                         sort_keys=True)))
        else:
            self._io.display("Problem calling the service. Response code: " +
                             str(response.status_code))
