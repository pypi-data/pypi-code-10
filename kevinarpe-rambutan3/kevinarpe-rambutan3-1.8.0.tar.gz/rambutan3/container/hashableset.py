# noinspection PyPep8Naming
class hashableset(set):

    def __hash__(self):
        x = hash(frozenset(self))
        return x
