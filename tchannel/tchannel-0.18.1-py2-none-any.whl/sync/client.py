# Copyright (c) 2015 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import

from threadloop import ThreadLoop

from tchannel import TChannel as AsyncTChannel


class TChannel(AsyncTChannel):
    """Make synchronous TChannel requests.

    This client does not support incoming requests -- it is a uni-directional
    client only.

    The client is implemented on top of the Tornado-based implementation and
    offloads IO to a thread running an ``IOLoop`` next to your process.

    Usage mirrors the :py:class:`TChannel` class.

    .. code-block:: python

        from tchannel.sync import TChannel

        tchannel = TChannel(name='my-synchronous-service')

        # Advertise with Hyperbahn.
        # This returns a future. You may want to block on its result,
        # particularly if you want you app to die on unsuccessful
        # advertisement.
        tchannel.advertise(routers)

        # keyvalue is the result of a call to ``tchannel.thrift.load``.
        future = tchannel.thrift(
            keyvalue.KeyValue.getItem('foo'),
            timeout=0.5,  #  0.5 seconds
        )

        result = future.result()

    Fanout can be accomplished by using ``as_completed`` from the
    ``concurrent.futures`` module:

    .. code-block:: python

        from concurrent.futures import as_completed

        from tchannel.sync import TChannel

        tchannel = TChannel(name='my-synchronous-service')

        futures = [
            tchannel.thrift(service.getItem(item))
            for item in ('foo', 'bar')
        ]

        for future in as_completed(futures):
            print future.result()

    (``concurrent.futures`` is native to Python 3; ``pip install futures`` if
    you're using Python 2.x.)

    """

    def __init__(
        self,
        name,
        hostport=None,
        process_name=None,
        known_peers=None,
        trace=False,
        threadloop=None,
    ):
        """Initialize a new TChannelClient.

        :param process_name:
            Name of the calling process. Used for logging purposes only.
        """
        super(TChannel, self).__init__(
            name,
            hostport=hostport,
            process_name=process_name,
            known_peers=known_peers,
            trace=trace,

        )
        self._threadloop = threadloop or ThreadLoop()
        self._threadloop.start()

        self.advertise = self._wrap(self.advertise)

        self.raw = self._wrap(self.raw)
        self.thrift = self._wrap(self.thrift)
        self.json = self._wrap(self.json)

    def _wrap(self, f):
        assert callable(f)

        def wrapper(*a, **kw):
            future = self._threadloop.submit(
                lambda: f(*a, **kw)
            )
            return future

        return wrapper

    def register(self, *a, **kw):
        raise NotImplementedError(
            "Registration not yet supported for sync clients",
        )
