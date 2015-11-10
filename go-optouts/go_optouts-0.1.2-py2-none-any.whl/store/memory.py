import uuid

from twisted.internet.defer import succeed
from zope.interface import implements

from .interface import IOptOutBackend, IOptOutCollection


class MemoryOptOutBackend(object):
    """ Memory opt out backend. """

    implements(IOptOutBackend)

    def __init__(self):
        self._collections = {}

    @classmethod
    def from_config(cls, _config):
        return cls()

    def get_opt_out_collection(self, owner_id):
        """ Return the opt out collection for the specified owner.

        :param str owner_id:
            The id of the owner of the opt out store.
        """
        collection = self._collections.get(owner_id)
        if collection is None:
            collection = self._collections[owner_id] = MemoryOptOutCollection()
        return collection


class MemoryOptOutCollection(object):
    """
    This implements the IOptOutStore interface.

    It stores the opt out in a dictionary using the address type
    and address as the key. The values are opt out objects, for example::

        {
            "id": "2468",
            "address_type": "msisdn",
            "address": "+273121100",
        }
    """

    implements(IOptOutCollection)

    def __init__(self):
        # _store maps (address_type, address) pairs to opt outs
        self._store = {}

    def get(self, address_type, address):
        key = (address_type, address)
        return succeed(self._store.get(key))

    def put(self, address_type, address):
        key = (address_type, address)
        opt_id = str(uuid.uuid4())
        self._store[key] = {
            'id': opt_id,
            'address_type': address_type,
            'address': address
        }
        return succeed(self._store.get(key))

    def delete(self, address_type, address):
        key = (address_type, address)
        return succeed(self._store.pop(key, None))

    def count(self):
        return succeed(len(self._store))
