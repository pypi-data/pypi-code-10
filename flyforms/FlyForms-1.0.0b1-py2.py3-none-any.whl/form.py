# coding=utf-8
from .core import Form, json


def from_json(form_cls, json_str, **kwargs):
    """
    Creates and returns new Form instance bound with data from passed json string

    :param form_cls: :py:class:`.Form` subclass
    :param json_str: json string
    :param kwargs: additional arguments for :code:`json.loads`
    :return: bound Form instantiated from :code:`form_cls`
    """

    if not issubclass(form_cls, Form):
        raise TypeError("Bad form type: expected Form subclass, got %s" % form_cls.__name__)

    return form_cls(**json.loads(json_str, **kwargs))


def validate_json(form_cls, json_str, **kwargs):
    """
    Validates given json string data within passed :py:class:`.Form` subclass by
    calling it`s :py:meth:`.Form.validate` classmethod.

    It is useful when you don`t need to load data from json to your Form.

    :param form_cls: :py:class:`.Form` subclass
    :param json_str: json string
    :param kwargs: additional arguments for :code:`json.loads`
    :return: bound Form instantiated from :code:`form_cls`
    """

    if not issubclass(form_cls, Form):
        raise TypeError("Bad form type: expected Form subclass, got %s" % form_cls.__name__)

    return form_cls.validate(**json.loads(json_str, **kwargs))


def to_json(form, **kwargs):
    """
    .. versionadded:: 1.0.0

    Dump Form data to json string

    :param form: instance of :py:class:`.Form` subclass
    :param kwargs: additional arguments passed to json.dumps

    :return: encoded json-string
    """

    if not issubclass(form, Form):
        raise TypeError("Bad form type: expected Form subclass, got %s" % type(form))

    return json.dumps(form.to_python(), **kwargs)