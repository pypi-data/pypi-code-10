import json


class Webhook(object):
    def __init__(self, attributes=None):
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = dict()
            self.attributes['event'] = None
            self.attributes['filter'] = None
            self.attributes['resource'] = None
            self.attributes['name'] = None
            self.attributes['targetUrl'] = None

    def set_event(self, val):
        self.attributes['event'] = val

    def get_event(self):
        return self.attributes['event']

    def set_filter(self, val):
        self.attributes['filter'] = val

    def get_filter(self):
        return self.attributes['filter']

    def set_resource(self, val):
        self.attributes['resource'] = val

    def get_resource(self):
        return self.attributes['resource']

    def set_name(self, val):
        self.attributes['name'] = val

    def get_name(self):
        return self.attributes['name']

    def set_targetUrl(self, val):
        self.attributes['targetUrl'] = val

    def get_targetUrl(self):
        return self.attributes['targetUrl']

    def get_json(self):
        return json.dumps(self.attributes)

    @classmethod
    def from_json(cls, obj):
        instance = cls(attributes=obj)
        return instance

    @classmethod
    def url(self):
        return '/webhooks'

    @classmethod
    def get(cls, session):
        items = session.get(cls.url()).json()['items']
        ret = []
        for i in items:
            obj = cls.from_json(i)
            ret.append(obj)
        return ret

    def create(self, session):
        resp = session.post(Webhook.url(), self.get_json())
        return resp

    def delete(self, session):
        url = self.get_url() + '/{}'.format(self.id)
        resp = session.delete(url)
        return resp


