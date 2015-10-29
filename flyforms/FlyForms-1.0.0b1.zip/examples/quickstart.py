# coding=utf-8

from flyforms.form import Form
from flyforms.fields import EmailField, StringField


class LoginForm(Form):
    email = EmailField()
    password = StringField(
        min_length=8,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])",
        max_length=64
    )


class RegistrationForm(LoginForm):

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


if __name__ == '__main__':
    form = LoginForm(
        email="qwerty@gmail.com",
        password="Qwerty_#123"
    )

    print(form.is_valid)  # >>> True
    print(form.errors)  # >>> {}

    print(form.password)  # >>> Qwerty_#123
    print(form.email)  # >>> qwerty@gmail.com
