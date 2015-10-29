# coding=utf-8
from flyforms import Form, IntField


class MyUnboundField(object):

    def __init__(self, *args, **kwargs):
        pass


class MyForm(Form):

    class Meta:
        skip_extra = True
        unbound_field_render = MyUnboundField

    field = IntField()
    not_required = IntField(required=False)


if __name__ == '__main__':
    f = MyForm(**{
        "field": 1,
        "extra_field1": None,
        "extra_field2": object()
    })

    print(f.is_valid)  # >> True
    print(f.to_python())  # >> {'field': 1}
    print(f.not_required)  # >> <__main__.MyUnboundField object at ...>
