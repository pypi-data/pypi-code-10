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


if __name__ == '__main__':

    # Valid data
    r1 = LoginForm.validate(email="smith@gmail.com", password="Qw3rT!y_")
    print(r1)  # >>>  True

    # Bad data
    r2 = LoginForm.validate(email="smith@gmail.com", password="Qwerty")
    print(r2)  # >>>  False
