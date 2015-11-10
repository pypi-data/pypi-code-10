class Plugin(object):
    def pre_handle(self, obj, field, sensei):
        # this method will be called by Sensei.
        # plugin must have it
        # do some pre-work (optionally)
        return self.handle(obj, field, sensei)

    def handle(self, obj, field, sensei):
        value = 'Independent Pretty Title'
        field.validate(value, obj)
        setattr(obj, field.attname, value)