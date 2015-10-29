# coding=utf-8
"""
This module contains a collection of fields classes
"""
from collections import Iterable, Callable
from datetime import datetime

from .common import jsonify_types, FrozenDict, UNSET
from .core import Form, Field
from .validators import *
from .compat import string_base, text_type

__all__ = (
    "StringField",
    "EmailField",
    "IntField",
    "FloatField",
    "BooleanField",
    "Ip4Field",
    "ListField",
    "ArrayField",
    "DatetimeField",
    "DictField",
    "EmbeddedFormField"
)


class SelectField(Field):
    """
    .. versionadded:: 1.0.0

    This is the base class for all Fields that reflect single values such as :code:`int`, :code:`float`, :code:`bool`
    and etc. It provides to specify list of valid values (choices). Any passed values which are not in the defined
    choices will cause validation fails.
    """

    def __init__(self, choices=(), **kwargs):
        """
        :param required: boolean flag is this field required or may be :py:data:`.UNSET`
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types

        :param choices: iterable object contains possible values of this field
        :type choices: Iterable

        """
        super(SelectField, self).__init__(**kwargs)

        # Add choices validation, if necessary
        if choices:
            self.base_validators.append(EntryValidator(choices, self.value_types))

    @Field.field_validation_hook
    def validate(self, value):
        pass


class StringField(SelectField):
    """
    Reflects Python strings
    """

    value_types = string_base  # valid types of field value
    wrapper = text_type

    def __init__(self, min_length=None, max_length=None, regex="", **kwargs):
        """
        :param required: boolean flag is this field required
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param min_length: the minimum length of the string
        :type min_length: int or None

        :param max_length: the maximum length of the string
        :type max_length: int or None

        :param regex: the regular expression to validate
        :type regex: str or regexp

        :param choices: iterable object contains possible values of this field
        :type choices: iterable

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """
        super(StringField, self).__init__(**kwargs)

        if min_length:
            self.base_validators.append(MinLengthValidator(min_length, False))

        if max_length:
            self.base_validators.append(MaxLengthValidator(max_length, False))

        if regex:
            self.base_validators.append(RegexValidator(regex))


class EmailField(StringField):
    """
    Reflects Python string corresponding to an email
    """

    def __init__(self, **kwargs):
        """
        :param required: boolean flag is this field required
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param choices: iterable object contains possible values of this field
        :type choices: iterable

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """
        super(EmailField, self).__init__(**kwargs)

        self.base_validators.append(EmailValidator())


class IntField(SelectField):
    """
    Reflects Python :code:`int` values
    """

    value_types = int  # valid types of field value

    def __init__(self, min_value=None, max_value=None, **kwargs):
        """
        :param required: boolean flag is this field required
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param min_value: the minimum valid value

        :param max_value: the maximum valid value

        :param choices: iterable object contains possible values of this field
        :type choices: iterable

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """
        super(IntField, self).__init__(**kwargs)

        if min_value is not None:
            self.base_validators.append(MinValueValidator(min_value, False))
        if max_value is not None:
            self.base_validators.append(MaxValueValidator(max_value, False))


class FloatField(IntField):
    """
    Reflects Python :code:`float` values
    """

    value_types = float  # valid types of field value


class BooleanField(SelectField):
    """
    Reflects Python :code:`bool` values
    """

    value_types = bool  # valid types of field value

    def __init__(self, **kwargs):
        """
        :param required: boolean flag is this field value may be :py:data:`.UNSET`
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """

        super(BooleanField, self).__init__(**kwargs)


class Ip4Field(StringField):
    """
    Reflects Python string corresponding to an IPv4 address
    """

    def __init__(self, **kwargs):
        """
        :param required: boolean flag is this field required
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param choices: iterable object contains possible values of this field
        :type choices: iterable

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types

        """

        super(Ip4Field, self).__init__(**kwargs)

        self.base_validators.append(Ip4AddressValidator())


class SequenceField(Field):
    """
    .. versionadded:: 1.0.0

    This is the base class for all Fields that reflect iterable values such as list, tuple and etc.
    It provides to specify such as minimum and maximum possible iterable length and validators for each item.
    """

    value_types = Iterable
    wrapper = tuple

    def __init__(self, min_length=None, max_length=None, item_validators=(), **kwargs):
        """
        :param required: boolean flag is this field required or may be :py:data:`.UNSET`
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types

        :param min_length: minimum iterable length
        :type min_length: int

        :param max_length: maximum iterable length
        :type max_length: int

        :param item_validators: the additional validators for every item
        :type item_validators: list of Callable

        """
        super(SequenceField, self).__init__(**kwargs)

        # Check is given item validators are callable object and extend validators list
        if any(not isinstance(validator, Callable) for validator in item_validators):
            raise TypeError("Each validator should be a callable object")
        self.item_validators = [validate_required] + list(item_validators)

        if min_length:
            self.base_validators.append(MinLengthValidator(min_length, False))

        if max_length:
            self.base_validators.append(MaxLengthValidator(max_length, False))

    @Field.field_validation_hook
    def validate(self, value):

        for item in value:  # run item validators
            for item_validator in self.item_validators:
                item_validator(item)


class ListField(SequenceField):
    """
    Reflects iterable Python objects
    """

    def __init__(self, jsonify=True, **kwargs):
        """
        :param required: boolean flag is this field required or may be :py:data:`.UNSET`
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param min_length: minimum iterable length
        :type min_length: int

        :param max_length: maximum iterable length
        :type max_length: int

        :param item_validators: the additional validators for every item
        :type item_validators: list of Callable

        :param jsonify: if True all items should be one of :py:data:`.jsonify_types`
        :type jsonify: bool

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """
        super(ListField, self).__init__(**kwargs)

        if jsonify:
            self.item_validators.append(TypeValidator(jsonify_types))


class ArrayField(SequenceField):
    """

    .. versionadded:: 0.2.0

    Reflects iterable objects where each item same type
    """

    def __init__(self, item_type, jsonify=True, **kwargs):
        """
        :param item_type: type of each item in the list

        :param required: boolean flag is this field required or may be :py:data:`.UNSET`
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param min_length: minimum iterable length
        :type min_length: int

        :param max_length: maximum iterable length
        :type max_length: int

        :param item_validators: the additional validators for every item
        :type item_validators: list of Callable

        :param jsonify: if True all items should be one of :py:data:`.jsonify_types`
        :type jsonify: bool

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """

        if jsonify and not any(issubclass(item_type, jsonify_type) for jsonify_type in jsonify_types):
            raise TypeError("Type %s is not supported for JSON encoding and decoding operations" % item_type)

        item_validators = kwargs.pop("item_validators", [])
        item_validators.append(TypeValidator(item_type))

        super(ArrayField, self).__init__(item_validators=item_validators, **kwargs)


class DatetimeField(Field):
    """
    .. versionadded:: 0.3.0

    A datetime field.

    Parse string contains datetime via datetime.strptime
    """

    value_types = string_base
    wrapper = text_type

    def __init__(self, required=True, fmt="%Y-%m-%d %H:%M:%S", now=False, null=False, validators=()):
        """
        :param required: boolean flag is this field value may be :py:data:`.UNSET`
        :type required: bool

        :param fmt: datetime format
        :type fmt: str

        :param now: if passed the default value will be datetime.now()
        :type now: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param validators: the additional validators for field
        :type validators: list of callable

        """

        default = datetime.now().strftime(self.fmt) if now else UNSET

        super(DatetimeField, self).__init__(required=required, null=null, validators=validators, default=default)

        self.fmt = fmt

    @Field.field_validation_hook
    def validate(self, value):

        try:
            datetime.strptime(value, self.fmt)
        except ValueError as error:
            raise ValidationError(error.message)


class DictField(Field):
    """

    .. versionadded:: 0.3.0

    Reflects Python dict
    """
    value_types = dict
    wrapper = FrozenDict

    def __init__(self, schema, **kwargs):
        """
        :param schema: template to dict validation
        :type schema: dict

        :param required: boolean flag is this field value may be :py:data:`.UNSET`
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types

        """

        if not isinstance(schema, dict):
            raise TypeError("Schema for DictField should be dict instance")

        for key, value in schema.items():
            if not isinstance(value, Field):
                raise TypeError(
                    "Bad field %s in schema. Expected Field subclass instance, got %s" % (
                        key, type(value)
                    )
                )

        super(DictField, self).__init__(**kwargs)
        self.schema = schema

    @Field.field_validation_hook
    def validate(self, value):

        d = dict(value)
        for key, field_obj in self.schema:
            field_obj.validate(d.pop(key, UNSET))
        if d != {}:
            raise ValidationError("Unknown fields: %s" % d.keys())

    @Field.field_binding_hook
    def bind(self, value):
        try:
            for validator in self.validators:  # run validators for whole dict
                validator(value)
        except ValidationError as e:  # if ValidationError occurred
            bound = UNSET
            error = e.message
        else:
            bound = {}
            error = {}
            d = dict(value)
            for key, field_obj in self.schema.items():
                bv, er = field_obj.bind(d.pop(key, UNSET))
                if er is None:
                    if bv is not UNSET:
                        bound[key] = bv
                    continue
                error[key] = er
            for unk in d:
                error[unk] = "Unknown field: %s" % unk
            bound = FrozenDict(bound)
            error = None if error == {} else error
        return bound, error


class EmbeddedFormField(Field):

    def __init__(self, form_cls, required=True, null=False):
        if not issubclass(form_cls, Form):
            raise TypeError("Bad form type: expected Form subclass, got %s" % form_cls.__name__)
        self.form_cls = form_cls

        super(EmbeddedFormField, self).__init__(required=required, null=null)

    # noinspection PyProtectedMember
    @Field.field_binding_hook
    def bind(self, value):
        d = dict(value)
        for field_name in self.form_cls._fields:
            field_obj = getattr(self.form_cls, field_name)
            try:
                field_obj.validate(d.pop(field_name, UNSET))
            except ValidationError as e:
                return UNSET, "%s.%s: %s" % (self.form_cls.__name__, field_name, e.message)
        if (not d) or self.form_cls._meta.skip_extra:
            return FrozenDict(**value), None
        return UNSET, "Unknown fields %s" % d.keys()

    @Field.field_validation_hook
    def validate(self, value):
        self.form_cls.validate(value)

