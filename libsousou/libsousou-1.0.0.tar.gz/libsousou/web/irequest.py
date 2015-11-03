

class IRequest(object):
    """Declares the basic interface for request objects used
    by the :mod:`libsousou.web` controllers.
    """

    def accepts_content_type(self, content_type):
        """Return a boolean indicating if the client accepts the
        given content type.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def get_request_method(self):
        """Return a string identifying the HTTP verb of the
        request.
        """
        raise NotImplementedError("Subclasses must override this method.")
