from untestable.arg_driven_app import ArgDrivenApp


class BitbucketApp(ArgDrivenApp):
    """
    A Bit Bucket argument driven application.
    """

    def __init__(self, io, *commands):
        self._io = io
        self._commands = commands

    def run(self, argv):
        if len(argv) == 0:
            message = ("No command provided. Nothing to do.\n" +
                       "Supported commands are:\n")

            for command in self._commands:
                message += command.name() + "\n"

            self._io.display(message)
            return

        # Find the command that can handle the request
        handled = False
        for command in self._commands:
            if command.can_handle(argv[0]):
                handled = True
                command.run()

        if not handled:
            self._io.display("Unrecognized command '" + argv[0] + "'")
