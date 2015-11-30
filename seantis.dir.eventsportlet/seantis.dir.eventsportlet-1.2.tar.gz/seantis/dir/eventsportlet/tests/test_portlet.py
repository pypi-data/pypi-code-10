from seantis.dir.eventsportlet.tests import IntegrationTestCase
from seantis.dir.eventsportlet.events import Renderer


class BrowserTestCase(IntegrationTestCase):

    def test_as_query_param(self):

        renderer = Renderer(None, None, None, None, None)

        self.assertEquals(renderer.as_query_param(None, None), '')
        self.assertEquals(renderer.as_query_param('', ''), '')
        self.assertEquals(renderer.as_query_param(None, 'value'), '')
        self.assertEquals(renderer.as_query_param('cat', None), '')
        self.assertEquals(renderer.as_query_param('', 'value'), '')

        self.assertEquals(renderer.as_query_param('cat', ''), '')
        self.assertEquals(renderer.as_query_param('cat', '\n\n \n'), '')
        self.assertEquals(renderer.as_query_param('cat', 'value'),
                          '&cat=value')
        self.assertEquals(renderer.as_query_param('cat', ' value'),
                          '&cat=value')
        self.assertEquals(renderer.as_query_param('cat', 'value\n'),
                          '&cat=value')
        self.assertEquals(renderer.as_query_param('cat', 'value \n '),
                          '&cat=value')
        self.assertEquals(renderer.as_query_param('cat', ' value \n '),
                          '&cat=value')
        self.assertEquals(renderer.as_query_param('cat', ' value1\n value2'),
                          '&cat=value1&cat=value2')
        self.assertEquals(renderer.as_query_param('cat', ' value1\n value2\n'),
                          '&cat=value1&cat=value2')
        self.assertEquals(
            renderer.as_query_param('cat', ' value1  \n value2\nvalue3'),
            '&cat=value1&cat=value2&cat=value3'
        )

        self.assertEquals(
            renderer.as_query_param('cat', ' value1  \n value 2\nvalue3'),
            '&cat=value1&cat=value+2&cat=value3'
        )
