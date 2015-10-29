# coding=utf-8
from abc import ABCMeta, abstractmethod
from collections import Iterable, Callable

try:
    import simplejson as json
except ImportError:
    import json

from .common import UNSET
from .compat import with_metaclass, itervalues, iteritems
from .validators import validate_not_null, validate_required, TypeValidator, ValidationError


class UnboundForm(Exception):
    """
    Raises when you try to serialize an :py:class:`.Form` bound with invalid data
    """
    pass


class Field(with_metaclass(ABCMeta, object)):
    """
    This is the base class for all builtin and user defined Fields.
    """

    value_types = type  # valid types of field value
    wrapper = None

    def __init__(self, required=True, null=False, validators=(), default=UNSET):
        """
        :param required: boolean flag is this field value may be :py:data:`.UNSET`
        :type required: bool

        :param null: boolean flag is field value may be :code:`None`
        :type null: bool

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types

        :raises TypeError: if passed arguments invalid
        """

        # Define validators container
        self.base_validators = []

        # Add not null validation, if necessary
        if null:
            self.base_validators.append(validate_not_null)
        self.null = null

        # Add required validation, if necessary
        if required:
            self.base_validators.append(validate_required)
        self.required = required

        # Check given default value
        if not isinstance(default, self.value_types) and default is not UNSET:
            raise TypeError(
                "Bad default value type. \nExpected {}, got {}".format(self.value_types, type(default))
            )
        self.default = default

        # Add type validation
        self.base_validators.append(TypeValidator(self.value_types))

        # Clean given list of validators, if necessary
        if not isinstance(validators, Iterable):
            raise TypeError("Validators should be an iterable object")

        # Check is given validators are callable object and extend validators list
        if any(not isinstance(validator, Callable) for validator in validators):
            raise TypeError("Each validator should be a callable object")
        self.custom_validators = list(validators)

    @property
    def validators(self):
        """
        .. versionchanged:: 1.0.0

        Generator that returns :code:`base_validators` and :code:`custom_validators` items successively
        """
        return (v for v in self.base_validators + self.custom_validators)

    @staticmethod
    def field_validation_hook(method):
        """
        Hook to avoid code duplicating in :py:meth:`Field.validate` method realizations
        that provides checking the value to :code:`None` and :py:data:`.UNSET`

        You may use it as decorator for :py:meth:`Field.validate` method in your custom fields
        """

        def wrapper(field_obj, value):
            assert isinstance(field_obj, Field)  # fixme debug
            if not field_obj.required and value is UNSET:  # check is value set
                return

            if field_obj.null and value is None:  # check for null
                return

            for validator in field_obj.validators:  # run validators for full sequence
                validator(value)

            method(field_obj, value)
        return wrapper

    @staticmethod
    def field_binding_hook(method):
        """
        Hook to avoid code duplicating in :py:meth:`Field.bind` method realizations
        that provides checking the value to :code:`None` and :py:data:`.UNSET`

        You may use it as decorator for :py:meth:`Field.bind` method in your custom fields
        """

        def wrapper(field_obj, value):
            assert isinstance(field_obj, Field)  # fixme debug
            if not field_obj.required and value is UNSET:  # check is value set
                return field_obj.default, None

            if field_obj.null and value is None:  # check is given value null
                return value, None

            return method(field_obj, value)

        return wrapper

    def bind(self, value):
        """
        .. versionadded:: 0.2.0

        .. versionchanged:: 1.0.0

        Validates given value via defined set of :code:`Validators`, wraps it into :py:attr:`.wrapper` and returns
        wrapped value and :code:`None` in second position.
        If some errors occurred returns an :py:data:`.UNSET` and this errors

        If value is mutable obj (for example :code:`list`) it'll be converted to immutable (for example :code:`tuple`)

        :param value: the value to bind
        :returns: bound value and occurred errors (if there were no errors - :code:`None` will be returned in second position)
        """

        if not self.required and value is UNSET:  # check is value set
            return self.default, None

        if self.null and value is None:  # check is given value null
            return value, None

        try:
            error = None

            for validator in self.validators:  # Run all validators
                validator(value)

            if self.wrapper is not None:  # Wrap value
                value = self.wrapper(value)
        except ValidationError as e:
            value = UNSET
            error = e.message
        return value, error

    @abstractmethod
    def validate(self, value):
        """
        Validates given value via defined set of :code:`Validators`
        """


class UnboundField(object):
    """
    Field without value
    """

    __slots__ = ("name", "field", "errors")

    def __init__(self, name, field_type, errors):
        """
        :param name: field name
        :param field_type: field class
        :param errors: field errors
        """
        self.name = name
        self.field = field_type
        self.errors = errors

    def __repr__(self):
        return "<Unbound{}({}, errors: {})>".format(self.field, self.name, self.errors)


class DefaultMetaOptions(object):
    skip_extra = False
    unbound_field_render = UnboundField


class FormMetaOptions(object):
    """
    Provides customization of :py:class:`.Form` instances behaviour.
    """

    def __init__(self, **kwargs):
        """
        .. py:attribute:: skip_extra

            (default: :code:`False`)
            if not defined, all extra field will be interpreted as errors during Form instantiation

        .. py:attribute:: unbound_field_render

            (default: :py:class:`.UnboundField`)
            all unbound Form fields will be replaced with instances of this class
        """

        self.skip_extra = kwargs.pop("skip_extra", DefaultMetaOptions.skip_extra)
        self.unbound_field_render = kwargs.pop("unbound_field_render", DefaultMetaOptions.unbound_field_render)
        self.kwargs = kwargs


class FormMeta(type):
    """
    The metaclass for Form and it's subclasses. It`s main responsibility
    - find all declared fields in the form and it`s bases.
    It also replaces the declared fields with :py:class:`.FormField` descriptor.
    """

    def __new__(mcs, name, bases, dct):

        # Parse meta options from defined Meta
        meta_opt_cls = dct.pop("Meta", DefaultMetaOptions)
        meta_opt = {k_opt: getattr(meta_opt_cls, k_opt) for k_opt in dir(meta_opt_cls) if not k_opt.startswith("_")}

        fields = []  # create a container for Form's fields names
        for attr, val in iteritems(dct):  # walk through class attributes
            if isinstance(val, Field):  # find all Field instances
                fields.append(attr)  # catch them
                dct[attr] = FormField(attr, val)  # and replace with descriptor

        # Update class attributes
        dct["_fields"] = set(fields)
        dct["_meta"] = FormMetaOptions(**meta_opt)

        cls = super(FormMeta, mcs).__new__(mcs, name, bases, dct)  # create new class

        # Get all fields names from MRO
        _fields = set()  # prepare container for Form fields names
        for base in cls.__mro__:  # walk through the MRO
            _fields |= getattr(base, "_fields", set())  # get fields names from each base
        cls._fields = _fields  # update Form's fields
        return cls


# noinspection PyProtectedMember
class FormField(object):
    """
    The descriptor for fields in :py:class:`.Form`. It`s behavior depends on whether the form is instantiated or not.
    """
    def __init__(self, name, field_obj):
        """
        :param name: declared field class attribute name
        :param field_obj: instance of declared field
        """

        if not isinstance(field_obj, Field):  # fixme debug
            raise TypeError("You should bind FormField with Field subclass instance, not {}".format(type(field_obj)))
        self.name = name
        self.field = field_obj

    def __get__(self, instance, owner):
        """
        If form is instantiated returns bound data, otherwise - instance of declared field
        """
        if not issubclass(owner, Form):  # fixme debug
            AttributeError("You can\'t use FormField without Form")
        if instance is None:
            return self.field
        return instance._raw_data.get(self.name, self.field.default)

    def __set__(self, instance, value):
        """
        Calls :py:meth:`.Field.bind` method and puts the result to :py:attr:`.Form._raw_data`.

        If :py:meth:`.Field.bind` returns :py:data:`.UNSET` value or there are errors
        (second return value is not :code:`None`) an instance of :py:class:`.UnboundField` will be
        put into :py:attr:`.Form._raw_data`.

        If form is instantiated :code:`AttributeError` will be raised.
        """
        if not isinstance(instance, Form):  # fixme debug
            raise AttributeError("You can\'t use FormField without Form")
        if self.name in instance._raw_data:
            raise AttributeError("You can\'t overwrite already bound field {}!".format(self.name))
        bound_value, errors = self.field.bind(value)
        if errors is not None:
            instance.errors[self.name] = errors
        if bound_value is UNSET:
            bound_value = instance._meta.unbound_field_render(self.name, self.field.__class__.__name__, errors)
        instance._raw_data[self.name] = bound_value

    def __delete__(self, instance):
        raise AttributeError("You can\'t delete Form fields!")


# noinspection PyProtectedMember
class Form(with_metaclass(FormMeta, object)):
    """
    The root class for all Forms
    """

    _fields = set()
    _meta = FormMetaOptions()

    def __init__(self, **data):
        """
        :param data: additional data to form
        :type data: dict

        When a Form is instantiated you can access given data via instance attributes or get everything at once
        using :py:meth:`.to_python()` method
        """
        self._raw_data = {}  # create a container for Form data
        self.errors = {}  # create a container for Form's errors

        for field_name in self._fields:  # walk through class fields
            setattr(self, field_name, data.pop(field_name, UNSET))  # and try to set up them

        if not self._meta.skip_extra:
            for unk in data:  # if some extra fields given it's an error
                self.errors[unk] = "Unknown field %s in data for Form %s" % (unk, self.__class__.__name__)

    @property
    def is_valid(self):
        """
        Checks is Form instance valid.
        Returns True if there are no errors. Otherwise, False.
        """
        return self.errors == {}

    @property
    def is_bound(self):
        """
        Checks is Form instance bound.
        Returns True if there are no :py:class:`.UnboundField` instances in :py:attr:`._raw_data`. Otherwise, False.
        """
        return not any(isinstance(v, UnboundField) for v in itervalues(self._raw_data))

    def to_python(self):
        """
        .. versionchanged:: 1.0.0

        .. versionadded:: 0.3.0

        Get form data as a :code:`dict`

        :returns: dictionary that contains bound data of valid form

        :raise UnboundForm: if :py:attr:`is_valid` returns False

        """
        if not self.is_valid:
            raise UnboundForm("Form bound with invalid data")
        return {f: self._raw_data[f] for f in self._fields
                if not isinstance(self._raw_data[f], self._meta.unbound_field_render)}

    @classmethod
    def validate(cls, **schema):
        """
        Class method provides data validation without :py:class:`.Form` instantiation by calling
        :py:meth:`.Field.validate` method of all declared fields

        :param schema: data to validate

        :return: boolean flag is data valid for this :py:class:`.Form`
        """
        d = dict(schema)
        for field_name in cls._fields:
            field_obj = getattr(cls, field_name)
            try:
                field_obj.validate(d.pop(field_name, UNSET))
            except ValidationError:
                return False
        if (not d) or cls._meta.skip_extra:
            return True
        return False
