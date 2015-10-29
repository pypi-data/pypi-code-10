# coding=utf-8
from flyforms.form import Form
from flyforms.fields import EmbeddedFormField, EmailField, StringField


class EmbeddedForm(Form):
    email = EmailField()
    password = StringField(
        min_length=8,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])",
        max_length=64
    )


class ContainerForm(Form):
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

    login_data = EmbeddedFormField(EmbeddedForm, null=True)

if __name__ == '__main__':
    f = ContainerForm(**{
        "first_name": "John",
        "last_name": "Smith",
        "login_data": {
            "email": "smith@gmail.com",
            "password": "Qw3rT!y_"
        }
    })

    print(f.is_bound)  # >>> True
    print(f.is_valid)  # >>> True
    print(f.errors)  # >>> {}
    print(f.to_python())
    print(f.login_data)  # >>> {'password': 'Qw3rT!y_', 'email': 'smith@gmail.com'}
    print(f.login_data.password)  # >>> Qw3rT!y_
