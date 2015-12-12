from syncgateway import urls


class Endpoint(object):

    def __init__(self, url, database, session):
        self.url = url
        self.database = database
        self.session = session

    @property
    def database_url(self):
        return urls.base_url(self.url, self.database)
