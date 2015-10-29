import warnings
from abc import (
    ABCMeta,
    abstractmethod,
    abstractproperty,
)
from six import with_metaclass

import pushalot.exc

class BaseAPI(with_metaclass(ABCMeta)):

    def __init__(self, token, transport):
        self._token = token
        self._transport = transport

    @abstractmethod # pragma: no cover
    def send(self, **kwargs):
        """
        Main method which should parse parameters
        and call transport send method
        """

    def get_api_params(self):
        """Dictionary with available API parameters

        :raises ValueError: If value of __class__.params is not dictionary
        :return: Should return dict with available pushalot API methods
        :rtype: dict
        """
        result = self.params
        if type(result) != dict:
            raise ValueError(
                '{}.params should return dictionary'.format(
                    self.__class__.__name__
                )
            )
        return result

    def get_api_required_params(self):
        """ List with required params

        :return: Dictionary with API parameters
        :raises ValueError: If value of __class__.required_params is not list
        :rtype: list
        """
        result = self.required_params
        if type(result) != list:
            raise ValueError(
                '{}.required_params should return list'.format(
                    self.__class__.__name__
                )
            )
        return result

    @abstractproperty # pragma: no cover
    def params(self):
        """Return dictionary with available API params

        Example of dictionary:
        {
            'token': {
                'param': 'AuthorizationToken',
                'type': str,
                'max_len': 32,
            },
            'is_important': {
                'param': 'IsImportant',
                'type': bool,
            },
            'ttl': {
                'param': 'TimeToLive',
                'type': int,
            }
        }

        Key of dictionary used as argument passed to function.
        param: in subdictionary is actual param which should be sent to API.
        type: type of the argument. Can be used for basic validation.
              Supported types now are boolean and string.
              All other types ignored, and used as is.
        max_len: Optional argument for string type. Check that length
                 of the passed argument not exceed the given maximum.

        :return: Dictionary with available API params
        :rtype: dict
        """

    @abstractproperty # pragma: no cover
    def required_params(self):
        """Return list with required API methods


        :return: List with required API methods
        """

    def _build_params_from_kwargs(self, **kwargs):
        """Builds parameters from passed arguments

        Search passed parameters in available methods,
        prepend specified API key, and return dictionary
        which can be sent directly to API server.


        :param kwargs:
        :type param: dict
        :raises ValueError: If type of specified parameter doesn't match
                            the expected type. Also raised if some basic
                            validation of passed parameter fails.
        :raises PushalotException: If required parameter not set.
        :return: Dictionary with params which can be
                 sent to API server
        :rtype: dict
        """
        api_methods = self.get_api_params()
        required_methods = self.get_api_required_params()
        ret_kwargs = {}
        for key, val in kwargs.items():
            if key not in api_methods:
                warnings.warn(
                    'Passed uknown parameter [{}]'.format(key),
                    Warning
                )
                continue
            if key not in required_methods and val is None:
                continue
            if type(val) != api_methods[key]['type']:
                raise ValueError(
                    "Invalid type specified to param: {}".format(key)
                )
            if 'max_len' in api_methods[key]:
                if len(val) > api_methods[key]['max_len']:
                    raise ValueError(
                        "Lenght of parameter [{}] more than "
                        "allowed length".format(key)
                    )
            ret_kwargs[api_methods[key]['param']] = val

        for item in required_methods:
            if item not in ret_kwargs:
                raise pushalot.exc.PushalotException(
                    "Parameter [{}] required, but not set".format(item)
                )

        return ret_kwargs


class APILatest(BaseAPI):

    def send(self, title, body,
             link_title=None, link=None, is_important=False,
             is_silent=False, image=None, source=None, ttl=None, **kwargs):
        """
        :param token: Service authorization token
        :type token: str
        :param title: Message title, up to 250 characters
        :type title: str
        :param body:  Message body, up to 32768 characters
        :type body: str
        :param link_title: Title of the link, up to 100 characters
        :type link: str
        :param link: Link URI, up to 1000 characters
        :type link: str
        :param is_important: Determines, is message important
        :type is_important: bool
        :param is_silent:  Prevents toast notifications on devices
        :type is_silent: bool
        :param image: Image URL link, up to 250 characters
        :type image: str
        :param source: Notifications source name, up to 25 characters
        :type source: str
        :param ttl: Message time to live in minutes (0 .. 43200)
        :type ttl: int
        :return: True on success
        """
        params = self._build_params_from_kwargs(
            token=self._token,
            title=title,
            body=body,
            link_title=link_title,
            link=link,
            is_important=is_important,
            is_silent=is_silent,
            image=image,
            source=source,
            ttl=ttl,
            **kwargs
        )
        return self._transport.send(**params)

    def send_message(self, title, body):
        """ Send message
        :param title: Message title
        :type title: str
        :param body:  Message body
        :type body: str
        :return: True on success
        :rtype: bool
        """
        return self.send(title=title, body=body)

    def send_silent_message(self, title, body):
        """ Send silent message
        :param title: Message title
        :type title: str
        :param body:  Message body
        :type body: str
        :return: True on success
        :rtype: bool
        """
        return self.send(title=title, body=body, is_silent=True)

    def send_important_message(self, title, body):
        """ Send important message
        :param title: Message title
        :type title: str
        :param body:  Message body
        :type body: str
        :return: True on success
        :rtype: bool
        """
        return self.send(title=title, body=body, is_important=True)

    def send_with_expiry(self, title, body, ttl):
        """ Send message with time to live
        :param title: Message title
        :type title: str
        :param body:  Message body
        :type body: str
        :param ttl: Time to live in minutes
        :type ttl: int
        :return: True on success
        :rtype: bool
        """
        return self.send(title=title, body=body, ttl=ttl)

    def send_with_link(self, title, body, link, link_title=None):
        """ Send message with link

        If no link title specified, URL used as title.

        :param title: Message title
        :type title: str
        :param body:  Message body
        :type body: str
        :param link: URL
        :type link: str
        :param link_title: URL title
        :type link_title: str
        :return: True on success
        :rtype: bool
        """
        link_title = link_title or link
        return self.send(
            title=title,
            body=body,
            link=link,
            link_title=link_title
        )

    def send_with_image(self, title, body, image):
        """ Send message with image

        Image thumbnail URL link, has to be properly formatted in absolute
        form with protocol etc. Recommended image size is 72x72 pixels.
        Larger images will be scaled down while maintaining aspect ratio.
        In order to save mobile device data plan, we download images
        from specified URL on server side and scale it there.
        This means client apps will never download big
        images directly by mistake.

        :param title: Message title
        :type title: str
        :param body:  Message body
        :type body: str
        :param image: URL to image
        :type image: str
        :return: True on success
        :rtype: bool
        """
        return self.send(title=title, body=body, image=image)

    @property
    def params(self):
        return {
            'token': {
                'param': 'AuthorizationToken',
                'type': str,
                'max_len': 32,
            },
            'title': {
                'param': 'Title',
                'type': str,
                'max_len': 250,
            },
            'body': {
                'param': 'Body',
                'type': str,
                'max_len': 32768,
            },
            'link_title': {
                'param': 'LinkTitle',
                'type': str,
                'max_len': 100,
            },
            'link': {
                'param': 'Link',
                'type':str,
                'max_len': 1000,
            },
            'is_important': {
                'param': 'IsImportant',
                'type': bool,
            },
            'is_silent': {
                'param': 'IsSilent',
                'type': bool,
            },
            'image': {
                'param': 'Image',
                'type': str,
                'max_len': 250,
            },
            'source': {
                'param': 'Source',
                'type': str,
                'max_len': 25,
            },
            'ttl': {
                'param': 'TimeToLive',
                'type': int,
            }
        }

    @property
    def required_params(self):
        return ['AuthorizationToken', 'Title', 'Body']
