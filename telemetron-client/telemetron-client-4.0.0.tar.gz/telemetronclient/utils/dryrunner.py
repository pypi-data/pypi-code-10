"""
DryRunner module
"""


class DryRunnerHandler(object):
    """ Dummy class to mock sockets and HTTPConnectionPool in dryRun mode """

    def __init__(self):
        self.msg = "(dryrun) %s() args=%s kws=%s"
        self.sent = []

    def _print(self, name, *args, **kws):
        """ Prints dryrun message """

        print self.msg % (name, args, kws)

    def sendall(self, *args, **kws):
        """ sendall mock """

        self._print('sendall', args, kws)
        self.sent.append((args, kws))
        if '_MOCK_FAILURE' in args[0]:
            raise Exception
        return None

    def sendto(self, *args, **kws):
        """ sendto mock """

        self._print('sendto', args, kws)
        self.sent.append((args, kws))
        if '_MOCK_FAILURE' in args[0]:
            return -1
        return len(args[0])

    def request(self, *args, **kws):
        """ request mock """

        self._print('request', args, kws)
        self.sent.append((args, kws))

        code = 201
        if '_MOCK_FAILURE' in kws['body']:
            code = 202

        class Result(object):
            """
            Dummy result
            """
            def __init__(self, code=201):
                self.status = code

        return Result(code)
