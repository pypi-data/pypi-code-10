# DictField nested usage
from flyforms.form import Form
from flyforms.fields import DictField, ListField, StringField, EmailField
from pprint import pprint


class MyForm(Form):
    field = DictField(
        schema={
            "list_field": ListField(),
            "nested_dict": DictField(
                schema={
                    "field1": EmailField(),
                    "field2": StringField(),
                    "nested_dd": DictField(
                        schema={
                            "email": EmailField(required=False)
                        }
                    )
                }
            )
        }
    )

if __name__ == '__main__':
    f = MyForm(
        field={
            "list_field": [0, 1, "Hello world!"],
            "nested_dict": {
                "field1": "qwerty@qwerty.com",
                "field2": "Hello world!",
                "nested_dd": {
                    "email": "qwerty@qwerty.com"
                }
            }
        }
    )

    print(f.is_valid)  # >>> True
    pprint(f.to_python())
