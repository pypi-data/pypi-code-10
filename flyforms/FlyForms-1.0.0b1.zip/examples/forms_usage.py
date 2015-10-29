# coding=utf-8
from flyforms.form import Form
from flyforms.fields import StringField, IntField

countries = (
    "United Kingdom",
    "United States",
    "Russia",
    "France",
    "Germany"
)


class GreetingForm(Form):
    first_name = StringField(
        regex=r"^[A-Z].*$",
        min_length=3,
        max_length=64
    )
    last_name = StringField(
        regex=r"^[A-Z].*$",
        min_length=3,
        max_length=64
    )

    country = StringField(choices=countries)

    company = StringField(
        required=False,
        default="Home"
    )

    age = IntField(min_value=18)


if __name__ == '__main__':
    form = GreetingForm(
        first_name="John",
        last_name="Smith",
        age=33,
        country="Germany"
    )

    print(form.is_valid)   # >>> True
    print(form.errors)   # >>> {}

    print(form.age)   # >>> 33
    print(form.company)   # >>> Home
