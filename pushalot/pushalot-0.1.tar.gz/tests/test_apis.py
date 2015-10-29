import unittest
import warnings

from pushalot.apis import (
    BaseAPI,
    APILatest,
)
from pushalot.exc import PushalotException
from pushalot.transport import (
    HTTPTransport,
    PushalotTransportInterface,
)

class DummyAPI(BaseAPI):

    def send(self, **kwargs):
        pass

    @property
    def params(self):
        return {
            'test_param': {
                'param': 'TestParam',
                'type': str,
                'max_len': 10
            }
        }

    @property
    def required_params(self):
        return ['TestParam']

class DummyAPIWithNoRequired(BaseAPI):

    def send(self, **kwargs):
        pass

    @property
    def params(self):
        return {
            'test_param': {
                'param': 'TestParam',
                'type': str,
                'max_len': 10
            }
        }

    @property
    def required_params(self):
        return []


class DummyAPIWithWrongParams(BaseAPI):

    def send(self, **kwargs):
        pass

    @property
    def params(self):
        return str

    @property
    def required_params(self):
        return []

class DummyAPIWithWrongRequiredParams(BaseAPI):

    def send(self, **kwargs):
        pass

    @property
    def params(self):
        return {}

    @property
    def required_params(self):
        return str


class DummyReturnTransport(PushalotTransportInterface):

    def send(self, **kwargs):
        return kwargs


class TestBaseAPI(unittest.TestCase):

    def test_api_init_set_up_token(self):
        api = DummyAPI(token='some-token', transport=None)
        self.assertTrue('_token' in api.__dict__)

    def test_api_init_set_up_token_correctly(self):
        api = DummyAPI(token='some-token', transport=None)
        self.assertEqual(api._token, 'some-token')

    def test_api_init_set_up_transport(self):
        api = DummyAPI(token='some-token', transport=None)
        self.assertTrue('_transport' in api.__dict__)

    def test_raises_if_params_has_wrong_value(self):
        with self.assertRaises(ValueError):
            api = DummyAPIWithWrongParams(token='some-token', transport=None)
            api.get_api_params()

    def test_raises_if_required_params_has_wrong_value(self):
        with self.assertRaises(ValueError):
            api = DummyAPIWithWrongRequiredParams(token='some-token', transport=None)
            api.get_api_required_params()

    def test_api_init_set_up_transport_correctly(self):
        transport = HTTPTransport()
        api = DummyAPI(token='some-token', transport=transport)
        self.assertEqual(api._transport, transport)

    def test_build_params_with_empty_kwargs_return_empty_dict(self):
        api = DummyAPIWithNoRequired(token='some-token', transport=None)
        result = api._build_params_from_kwargs()
        self.assertDictEqual(result, {})

    def test_build_params_raise_exception_if_required_param_not_specified(self):
        with self.assertRaises(PushalotException):
            api = DummyAPI(token='some-token', transport=None)
            result = api._build_params_from_kwargs()
            self.assertDictEqual(result, {})

    def test_build_params_with_kwargs_returns_correct_dict(self):
        api = DummyAPI(token='some-token', transport=None)
        result = api._build_params_from_kwargs(test_param='Test')
        self.assertDictEqual(result, {'TestParam': 'Test'})

    def test_build_params_uses_param_name_in_return(self):
        api = DummyAPI(token='some-token', transport=None)
        result = api._build_params_from_kwargs(test_param='Test')
        self.assertTrue('TestParam' in result)

    def test_build_params_raise_exception_if_invalid_type_of_param(self):
        with self.assertRaises(ValueError):
            api = DummyAPI(token='some-token', transport=None)
            result = api._build_params_from_kwargs(test_param=True)

    def test_build_params_respect_max_len_in_str_api_method(self):
        with self.assertRaises(ValueError):
            api = DummyAPI(token='some-token', transport=None)
            result = api._build_params_from_kwargs(
                test_param='Test-string-longer-than-10-chars'
            )

    def test_build_params_ignores_and_not_return_unkown_params(self):
        api = DummyAPI(token='some-token', transport=None)
        result = api._build_params_from_kwargs(
            test_param='Test',
            unknown_test_param='Test'
        )
        self.assertDictEqual(result, {'TestParam': 'Test'})

    def test_build_param_warns_on_unkown_api_method(self):
        with warnings.catch_warnings(record=True) as w:
            api = DummyAPI(token='some-token', transport=None)
            result = api._build_params_from_kwargs(
                test_param='Test',
                unknown_test_param='Test'
            )
            self.assertEqual(len(w), 1)


class TestAPILatest(unittest.TestCase):

    def _param_builder(self, api, silent=False, important=False, **kwargs):
        return api._build_params_from_kwargs(
            token=api._token,
            is_silent=silent,
            is_important=important,
            **kwargs
        )

    def test_send_uses_build_params_for_parameters_building(self):
        api = APILatest(token='some-token', transport=DummyReturnTransport())
        self.assertDictEqual(
            api.send('Test', 'Test'),
            api._build_params_from_kwargs(
                token='some-token',
                title='Test',
                body='Test',
                is_important=False,
                is_silent=False
            )
        )

    def test_send_message_calls_send(self):
        api = APILatest(token='some-token', transport=DummyReturnTransport())
        self.assertDictEqual(
            api.send_message('test', 'test'),
            self._param_builder(api=api, title='test', body='test')
        )

    def test_send_silent_message(self):
        api = APILatest(token='some-token', transport=DummyReturnTransport())
        self.assertDictEqual(
            api.send_silent_message('test', 'test'),
            self._param_builder(api=api, title='test', body='test', silent=True)
        )

    def test_send_important_message(self):
        api = APILatest(token='some-token', transport=DummyReturnTransport())
        self.assertDictEqual(
            api.send_important_message('test', 'test'),
            self._param_builder(api=api, title='test', body='test', important=True)
        )

    def test_send_with_expiry(self):
        api = APILatest(token='some-token', transport=DummyReturnTransport())
        self.assertDictEqual(
            api.send_with_expiry('test', 'test', ttl=1),
            self._param_builder(api=api, title='test', body='test', ttl=1)
        )

    def test_send_with_link_title(self):
        api = APILatest(token='some-token', transport=DummyReturnTransport())
        self.assertDictEqual(
            api.send_with_link(
                'test',
                'test',
                link='http://the-bosha.ru',
                link_title='blog'
            ),
            self._param_builder(
                api=api,
                title='test',
                body='test',
                link='http://the-bosha.ru',
                link_title='blog'
            )
        )

    def test_send_with_link_without_link_title(self):
        api = APILatest(token='some-token', transport=DummyReturnTransport())
        self.assertDictEqual(
            api.send_with_link(
                'test',
                'test',
                link='http://the-bosha.ru'
            ),
            self._param_builder(
                api=api,
                title='test',
                body='test',
                link='http://the-bosha.ru',
                link_title='http://the-bosha.ru'
            )
        )

    def test_send_with_icon(self):
        api = APILatest(token='some-token', transport=DummyReturnTransport())
        self.assertDictEqual(
            api.send_with_image(
                'test',
                'test',
                image='http://the-bosha.ru/favicon.ico'
            ),
            self._param_builder(
                api=api,
                title='test',
                body='test',
                image='http://the-bosha.ru/favicon.ico',
            )
        )
