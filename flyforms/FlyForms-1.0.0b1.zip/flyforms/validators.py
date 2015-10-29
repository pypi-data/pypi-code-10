# coding=utf-8
from abc import ABCMeta, abstractmethod
from collections import Iterable
import re

from .common import UNSET
from .compat import with_metaclass

__all__ = (
    "EntryValidator",
    "MaxValueValidator",
    "MaxLengthValidator",
    "MinLengthValidator",
    "MinValueValidator",
    "EmailValidator",
    "RegexValidator",
    "Ip4AddressValidator",
    "RequiredValidator",
    "TypeValidator",
    "ValidationError",
    "validate_required",
    "validate_email",
    "validate_ip",
    "validate_not_null"
)


class ValidationError(Exception):
    """
    Raised when a validator fails to validate it's input.
    """
    pass


class Validator(with_metaclass(ABCMeta, object)):
    """
    The abstract root class for all Validators.
    """

    __slots__ = ()

    message = ""

    @abstractmethod
    def __call__(self, value):
        """
        Validate the given value

        :param value: given value to validate

        :raises ValidationError: if given value is not valid
        """
        pass


class SimpleValidator(with_metaclass(ABCMeta, Validator)):
    """
    The Validator's subclass with only one validation case.
    Given value should satisfies condition in :py:meth:`validation_case` method
    """
    __slots__ = ()

    validation_case = abstractmethod(lambda self, x: x is x)  # Given value should satisfies this condition

    def __call__(self, value):
        if not self.validation_case(value):  # check validation case
            raise ValidationError(self.message)  # and raise ValidationError if result is not match


class RequiredValidator(SimpleValidator):
    """
    Validates is given value not :py:data:`.UNSET` object
    """
    __slots__ = ()

    message = "Field is required"

    validation_case = lambda self, value: value is not UNSET


class TypeValidator(SimpleValidator):
    """
    Validates is given value instance of passed :code:`value_types`
    """
    __slots__ = ("value_types",)

    message = "Bad value type"

    def __init__(self, value_types):
        """
        :param value_types: list of possible value types
        """
        self.value_types = value_types

    validation_case = lambda self, value: isinstance(value, self.value_types) or value is UNSET


class EntryValidator(SimpleValidator):
    """
    Validates is given value in specified during initialization iterable object
    """

    __slots__ = ("iterable",)

    message = "Value not in choices."

    def __init__(self, iterable, item_type=None):
        """
        :param iterable: the iterable object

        :raise: TypeError if given object is not iterable
        """
        if not isinstance(iterable, Iterable):
            raise TypeError("Entry validator instance need an iterable object")
        if item_type is not None and any(not isinstance(item, item_type) for item in iterable):
            raise TypeError("Bad type object found in given iterable")

        self.iterable = iterable

    validation_case = lambda self, value: value in self.iterable


class MinValueValidator(SimpleValidator):
    """
    Validates is given value greater than specified during initialization value
    """

    __slots__ = ("min_value", "strong")

    message = "Given value is less than minimum valid value."

    def __init__(self, min_value, strong=True):
        """
        :param min_value: the minimum valid value

        :param strong: boolean flag should be comparison strict or not
        :type strong: bool
        """
        self.min_value = min_value
        self.strong = strong

    validation_case = lambda self, value: value > self.min_value if self.strong else value >= self.min_value


class MaxValueValidator(SimpleValidator):
    """
    Validates is given value less than specified during initialization value
    """

    __slots__ = ("max_value", "strong")

    message = "Given value is greater than maximum valid"

    def __init__(self, max_value, strong=True):
        """
        :param max_value: the maximum valid value

        :param strong: boolean flag should be comparison strict or not
        :type strong: bool
        """
        self.max_value = max_value
        self.strong = strong

    validation_case = lambda self, value: value < self.max_value if self.strong else value <= self.max_value


class MinLengthValidator(SimpleValidator):
    """
    Validates the minimum object length
    """
    __slots__ = ("len", "strong")

    message = "Value length less than minimum valid"

    def __init__(self, min_length, strong=True):
        """
        :param min_length: the minimum valid length

        :param strong: boolean flag should be comparison strict or not
        :type strong: bool
        """
        self.len = min_length
        self.strong = strong

    def __call__(self, value):
        if not hasattr(value, '__len__'):  # check for __len__ attribute
            raise ValidationError("Validation failed because value of type '%s' has no length" % type(value))
        super(MinLengthValidator, self).__call__(len(value))

    validation_case = lambda self, value_len: value_len > self.len if self.strong else value_len >= self.len


class MaxLengthValidator(MinLengthValidator):
    """
    Validates the maximum object length
    """
    __slots__ = ("len", "strong")

    message = "Value length greater than maximum valid"

    def __init__(self, max_length, strong=True):
        """
        :param max_length: the maximum valid length

        :param strong: boolean flag should be comparison strict or not
        :type strong: bool
        """
        super(MaxLengthValidator, self).__init__(max_length, strong)

    validation_case = lambda self, value_len: value_len < self.len if self.strong else value_len <= self.len


class RegexValidator(SimpleValidator):
    """
    Validates string matching with regular expression
    """

    __slots__ = ("r",)

    message = "Value does not match the regular expression."

    def __init__(self, regex, flags=0):
        """
        :param regex: the regular expression

        :param flags: flags passed to re.match function
        """
        self.r = re.compile(regex, flags)

    def __call__(self, value):
        """
        The Validator's validate method implementation
        """
        super(RegexValidator, self).__call__(value)

    validation_case = lambda self, value: self.r.match(value)


class EmailValidator(RegexValidator):
    """
    Validates an email address via simple regex.
    """

    __slots__ = ()

    message = "Bad e-mail address"

    def __init__(self):
        super(EmailValidator, self).__init__(
            regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )


class Ip4AddressValidator(RegexValidator):
    """
    Validates an IPv4 address via simple regex.
    """

    __slots__ = ()

    message = "Bad ip address"

    def __init__(self):
        super(Ip4AddressValidator, self).__init__(
            regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        )


def validate_email(email):
    """
    Validates an email address via simple regex.
    """
    if not re.match(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", string=email):
        raise ValidationError("Bad e-mail address")


def validate_ip(ip):
    """
    Validates an IPv4 address via simple regex.
    """
    if not re.match(pattern=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", string=ip):
        raise ValidationError("Bad ip address")


def validate_required(value):
    """
    Validates is given value not :py:data:`.UNSET` object
    """
    if value is UNSET:
        raise ValidationError("Field is required")


def validate_not_null(value):
    """
    Validates is given value not :code:`None`
    """
    if value is None:
        raise ValidationError("Field is required")