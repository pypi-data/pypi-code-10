# coding=utf-8
from flyforms.fields import StringField
from flyforms.validators import RegexValidator, ValidationError
from unittest import main, TestCase


class HexField(StringField):
    """
    Reflects hex colors
    """

    def __init__(self, **kwargs):
        super(HexField, self).__init__(**kwargs)  # do not forget to call superclass constructor

        self.base_validators.append(RegexValidator(regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"))


class TestHexField(TestCase):
    def test(self):
        valid_data = ["#fff", "#fffaaa"]
        invalid_data = ["#fffaa", "fffaaa"]

        for v_value in valid_data:
            HexField().validate(v_value)

        for i_value in invalid_data:
            with self.assertRaises(ValidationError):
                HexField().validate(i_value)


if __name__ == '__main__':
    main()  # OK
