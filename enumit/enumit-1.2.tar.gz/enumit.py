"""
Enumeration class for python.

Usage:
    Status(Enum):
        APPROVED = Enum.Field('approved')
        DENIED = Enum.Field('denied', 'Denied')

    >> Status.APPROVED
    >> approved

    >> Status['approved']
    >> Approved

    >> Status.choices()
    >> [('approved', 'Approved'), ('denied', 'Denied')]

    >> Status.values()
    >> ['approved', 'denied']

    >> Status.names()
    >> ['Approved', 'Denied']

    >> 'approved' in Status
    >> True
"""

__all__ = ['Enum']


class EnumField(object):
    __counter__ = 0

    def __init__(self, value, name=None):
        self.value = value
        self.name = name

        # necessary to get enum members in defined orders.
        EnumField.__counter__ += 1
        self.__counter__ = EnumField.__counter__

    def set_name_by_attr(self, attr_name):
        self.name = ' '.join([i.capitalize() for i in attr_name.split('_')])


class EnumMeta(type):
    def __new__(mcs, name, bases, attributes):
        new_class = super(EnumMeta, mcs).__new__(mcs, name, bases, attributes)

        parents = [b for b in bases if isinstance(b, EnumMeta)]
        if not parents:
            return new_class

        new_class.members = list()
        new_class._member_attr_names = list()
        for attr_name, obj in attributes.items():
            if not isinstance(obj, EnumField):
                continue

            if obj.name is None:
                obj.set_name_by_attr(attr_name)

            new_class.members.append((obj.value, obj))
            # override the class attribute with own value
            setattr(new_class, attr_name, obj.value)

            new_class._member_attr_names.append(attr_name)

        new_class.members = sorted(new_class.members, key=lambda item: item[1].__counter__)

        for base in bases:
            if isinstance(base, EnumMeta):
                new_class.members = getattr(base, 'members', []) + new_class.members

        return new_class

    def __getitem__(cls, item):
        return dict(cls.members)[item].name

    def __setattr__(cls, key, value):
        if key in getattr(cls, '_member_attr_names', []):
            raise ValueError('Enum field can not be changed.')

        super(EnumMeta, cls).__setattr__(key, value)

    def __delattr__(cls, item):
        if item in getattr(cls, '_member_attr_names', []):
            raise ValueError('Enum field can not be deleted.')

        super(EnumMeta, cls).__delattr__(item)

    def __contains__(cls, item):
        return item in [value for value, __ in cls.members]

    def __iter__(cls):
        return (value for value, __ in cls.members)

    def __len__(cls):
        return len(cls.members)

    def __repr__(cls):
        return '<Enum %r>' % cls.__name__


class EnumBase(object):
    Field = EnumField
    members = list()

    @classmethod
    def choices(cls):
        return [(member.value, member.name) for __, member in cls.members]

    @classmethod
    def values(cls):
        return [member.value for __, member in cls.members]

    @classmethod
    def names(cls):
        return [member.name for __, member in cls.members]


# Metaclass definition to work with both python 2.7 and 3.
Enum = EnumMeta('Enum', (EnumBase, ), dict())
