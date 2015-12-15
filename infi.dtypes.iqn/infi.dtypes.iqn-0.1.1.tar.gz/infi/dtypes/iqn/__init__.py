class IQN(object):
    def __init__(self, name):
        super(IQN, self).__init__()
        if isinstance(name, IQN):
            self._name = name._name
        else:
            self._name = name
        fields = self._name.split(':')
        base, self._extra = fields[0], tuple(fields[1:])
        base_fields = base.split('.')
        self._type = base_fields[0]
        self._date = base_fields[1]
        self._naming_authority = '.'.join(base_fields[2:])
        assert self._type == 'iqn'

    def __repr__(self):
        return self._name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        if not isinstance(other, IQN):
            try:
                other = IQN(other)
            except:
                return False
        return self._name == other._name

    def __ne__(self, other):
        return not (self == other)

    def get_date(self):
        return self._date

    def get_naming_authority(self):
        return self._naming_authority

    def get_extra(self):
        return ':'.join(self._extra)

    def get_extra_fields(self):
        return self._extra
