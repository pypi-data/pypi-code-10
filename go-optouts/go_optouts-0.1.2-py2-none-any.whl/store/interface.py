import zope.interface


class IOptOutBackend(zope.interface.Interface):
    def get_opt_out_collection(owner_id):
        """ Return the opt out collection for the specified owner.

        :param str owner_id:
            The id of the owner of the opt out store.
        """


class IOptOutCollection(zope.interface.Interface):

        def get(address_type, address):
            """ Retrieve the opt out for an address. """

        def put(address_type, address):
            """ Store a record of an opt out for an address. """

        def delete(address_type, address):
            """ Remove an opt out for an address. """

        def count():
            """ Return the number of opt outs. """
