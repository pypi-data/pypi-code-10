class Route:
    def __init__(self, regex, method='GET', authorization=True):
        self.regex = regex
        self.method = method
        self.authorization = authorization


routes = {
    'ping': Route('/?expressly/api/ping/?', authorization=False),
    'registered': Route('/?expressly/api/registered/?'),
    'user': Route('/?expressly/api/user/(?P<email>[0-9a-zA-Z\-\_]+\@[0-9a-zA-Z\-\_\.]+)/?', authorization=False),
    'migration_popup': Route(
        '/?expressly/api/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/?'),
    'migration_user': Route(
        '/?expressly/api/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/migrate/?'),
    'batch_customer': Route('/?expressly/api/batch/customer/?', 'POST'),
    'batch_invoice': Route('/?expressly/api/batch/invoice/?', 'POST')
}
