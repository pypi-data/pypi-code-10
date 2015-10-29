# ArrayField usage
from flyforms.form import Form
from flyforms.fields import StringField, ArrayField


class CommentForm(Form):
    login = StringField()
    comment = StringField(max_length=256)
    tags = ArrayField(item_type=str)

if __name__ == '__main__':
    f = CommentForm(
        login="YourLogin",
        comment="Your comment",
        tags=["schema", "python", "json"]  # <-- list
    )

    print(f.is_valid)  # >>> True
    print(f.errors)  # >>> {}
    print(f.to_python())

    # Given list was wrapped into tuple
    print(type(f.tags))  # >>> <type 'tuple'>
