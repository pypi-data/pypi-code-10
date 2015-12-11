import json
import spark.messages


class Room(object):
    def __init__(self, attributes=None):
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = dict()
            self.attributes['sipAddress'] = None
            self.attributes['created'] = None
            self.attributes['id'] = None
            self.attributes['title'] = None

    def __str__(self):
        return self.attributes['title']

    @property
    def sipAddress(self):
        return self.attributes['sipAddress']

    @sipAddress.setter
    def sipAddress(self, val):
        self.attributes['sipAddress'] = val

    @property
    def created(self):
        return self.attributes['created']

    @created.setter
    def created(self, val):
        self.attributes['created'] = val
    @property
    def id(self):
        return self.attributes['id']

    @id.setter
    def id(self, val):
        self.attributes['id'] = val

    @property
    def title(self):
        return self.attributes['title']

    @title.setter
    def title(self, val):
        self.attributes['title'] = val

    @classmethod
    def url(cls):
        return '/rooms'

    def create(self, session):
        url = self.url()
        resp = session.post(url, self.json())

        #update attributes after creating
        data = resp.json()
        self.id = data['id']
        self.created = data['created']
        return resp

    def delete(self, session):
        url = self.url() + '/{}'.format(self.id)
        resp = session.delete(url)
        return resp

    def json(self):
        return json.dumps(self.attributes)

    def send_message(self, session, msg):
        if isinstance(msg, spark.messages.Message):
            message = msg
        else:
            message = spark.messages.Message()
            message.text = msg
        message.roomId = self.id
        resp = session.post('/messages', message.json())
        return resp

    def get_messages(self, session):
        url = '/messages?roomId={}'.format(self.id)
        resp = session.get(url)

        ret = []
        for msg in resp.json()['items']:
            obj = spark.messages.Message(attributes=msg)
            ret.append(obj)
        return ret

    @classmethod
    def get(cls, session, name=None):
        """
        Retrieve room list
        :param session: Session object
        :return: list rooms available in the current session
        """
        ret = []
        rooms = json.loads(session.get(cls.url()).text)['items']
        for room in rooms:
            obj = cls.from_json(room)
            if name == obj.title:
                return obj
            else:
                ret.append(obj)
        return ret

    @classmethod
    def from_json(cls, obj):
        if isinstance(obj, dict):
            obj = cls(attributes=obj)
        elif isinstance(obj, (str, unicode)):
            obj = cls(attributes=json.loads(obj))
        else:
            raise TypeError('Data must be str or dict')
        return obj