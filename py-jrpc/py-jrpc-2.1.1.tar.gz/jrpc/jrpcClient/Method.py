
__author__ = 'umairghani'

class _Method(object):
    """
    some magic to bind a  method to the server.
    supports "nested" methods (e.g. examples.getStateName)
    """
    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, "%s.%s" % (self.__name, name))

    def __call__(self, *args):
        return self.__send(self.__name, args)
