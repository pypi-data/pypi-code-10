from flyforms import Form, IntField


class GrandParent(Form):
    grandparent_field = IntField()


class Parent(GrandParent):
    parent_field = IntField()


class Child(Parent):
    child_field = IntField()


if __name__ == '__main__':
    print(Child._fields)  # >> set(['parent_field', 'child_field', 'grandparent_field'])
