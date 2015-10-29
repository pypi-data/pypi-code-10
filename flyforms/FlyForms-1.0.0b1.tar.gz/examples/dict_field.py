# DictField usage
from flyforms.form import Form
from flyforms.fields import DictField, EmailField, StringField


class MyForm(Form):
    cred = DictField(
        schema={
            "email": EmailField(),
            "password": StringField(
                min_length=8,
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])",
                max_length=64
            )
        }
    )


if __name__ == '__main__':
    f = MyForm(
        cred={
            "email": "qwerty@gmail.com",
            "password": "Qwerty_#123"
        }  # <--- dict
    )

    print(f.is_valid)  # >>> True
    print(f.errors)  # >>> {}
    print(f.cred)   # >>> {'password': 'Qwerty_#123', 'email': 'qwerty@gmail.com'}
    print(type(f.cred))  # >>> <class 'flyforms.common.FrozenDict'>  <--- !!!
