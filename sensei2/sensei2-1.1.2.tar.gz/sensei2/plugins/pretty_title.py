from sensei2.sensei.field_handlers import BaseHandler


class Plugin(BaseHandler):
    def prepare_value(self, obj, field, sensei):
        return 'Pretty title'