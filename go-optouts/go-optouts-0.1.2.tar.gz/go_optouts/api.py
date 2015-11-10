import json

from klein import Klein
from twisted.internet.defer import inlineCallbacks, returnValue


class OwnerIdNotValid(Exception):
    """ Raised when no valid owner is found. """


class OptOutNotFound(Exception):
    """ Raised when no opt out is found. """


class OptOutAlreadyExists(Exception):
    """ Raised when opt out already exists. """


class OptOutNotDeleted(Exception):
    """ Raised when opt out not deleted. """


class API(object):
    app = Klein()

    def __init__(self, backend, auth):
        self._backend = backend
        self._auth = auth

    def response(self, request, status_code=200, status_reason="OK", **data):
        request.setResponseCode(status_code)
        request.setHeader('Content-Type', 'application/json')
        data.update({
            "status": {
                "code": status_code,
                "reason": status_reason,
            },
        })
        return json.dumps(data)

    @inlineCallbacks
    def collection(self, request):
        owner_id = yield self._auth.owner_id(request)
        if owner_id is None:
            raise OwnerIdNotValid()
        returnValue(self._backend.get_opt_out_collection(owner_id))

# Error Handling

    @app.handle_errors(OwnerIdNotValid)
    def owner_id_not_valid(self, request, failure):
        return self.response(
            request, status_code=401, status_reason="Owner ID not valid.")

    @app.handle_errors(OptOutNotFound)
    def opt_out_not_found(self, request, failure):
        return self.response(
            request, status_code=404, status_reason="Opt out not found.")

    @app.handle_errors(OptOutAlreadyExists)
    def opt_out_already_exists(self, request, failure):
        return self.response(
            request, status_code=409, status_reason="Opt out already exists.")

    @app.handle_errors(OptOutNotDeleted)
    def opt_out_not_deleted(self, request, failure):
        return self.response(
            request, status_code=404,
            status_reason="There\'s nothing to delete.")

# Methods

    @app.route('/<string:addresstype>/<string:address>',
               methods=['GET'])
    @inlineCallbacks
    def get_address(self, request, addresstype, address):
        collection = yield self.collection(request)
        opt_out = yield collection.get(addresstype, address)
        if opt_out is None:
            raise OptOutNotFound()
        returnValue(self.response(request, opt_out=opt_out))

    @app.route('/<string:addresstype>/<string:address>',
               methods=['PUT'])
    @inlineCallbacks
    def save_address(self, request, addresstype, address):
        collection = yield self.collection(request)
        opt_out = yield collection.get(addresstype, address)
        if opt_out is not None:
            raise OptOutAlreadyExists()
        opt_out = yield collection.put(addresstype, address)
        returnValue(self.response(request, opt_out=opt_out))

    @app.route('/<string:addresstype>/<string:address>',
               methods=['DELETE'])
    @inlineCallbacks
    def delete_address(self, request, addresstype, address):
        collection = yield self.collection(request)
        opt_out = yield collection.delete(addresstype, address)
        if opt_out is None:
            raise OptOutNotDeleted()
        returnValue(self.response(request, opt_out=opt_out))

    @app.route('/count', methods=['GET'])
    @inlineCallbacks
    def get_opt_out_count(self, request):
        collection = yield self.collection(request)
        count = yield collection.count()
        returnValue(self.response(request, opt_out_count=count))
