from flyforms import Form, IntField, EmailField


class GrandParent(Form):
    grandparent = IntField()


class Mother(GrandParent):
    mother = IntField()
    parent = EmailField()


class Father(GrandParent):
    father = IntField()
    parent = IntField()


class Child(Mother, Father):
    child = IntField()


if __name__ == '__main__':
    print(Child._fields)  # >> set(['parent', 'mother', 'grandparent', 'child', 'father'])
    print(Child.parent)  # >> <flyforms.fields.EmailField object at ...>
