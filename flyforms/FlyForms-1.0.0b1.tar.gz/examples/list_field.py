# coding=utf-8
from flyforms.form import Form
from flyforms.fields import ListField
from flyforms.common import UNSET


class ListForm(Form):
    jsonify_list = ListField(min_length=2, max_length=5)
    common_list = ListField(min_length=3, jsonify=False)

if __name__ == '__main__':
    form = ListForm(
        jsonify_list=["Hello!", 2.5, 0],
        common_list=[object(), 500, "... world!", UNSET]
    )

    print(form.is_valid)   # >>> True
    print(form.errors)   # >>> {}
