from fnny import pluck, method, partial


class _Argless(object):
    def wow(self):
        return 100


class _OneArg(object):
    def add(self, n):
        return 100 + n


class _OneKwarg(object):
    def derp(self, something="yes"):
        return "lol" + something


def test_plucker():
    from collections import namedtuple
    G = namedtuple("G", ["a"])
    guys = [G(i) for i in range(10)]
    assert sum(map(lambda x: x.a, guys)) == sum(map(pluck.a, guys))


def test_method():
    no_args = [_Argless() for a in range(10)]
    expected = list(map(lambda x: x.wow(), no_args))
    actual = list(map(method.wow, no_args))
    assert expected == actual


def test_partial():
    has_args = [_OneArg() for a in range(10)]
    expected = list(map(lambda x: x.add(1), has_args))
    actual = list(map(partial.add(1), has_args))
    assert expected == actual


def test_partial_kwarg():
    has_args = [_OneKwarg() for a in range(10)]
    expected = list(map(lambda x: x.derp(something="heyy"), has_args))
    actual = list(map(partial.derp(something="heyy"), has_args))
    assert expected == actual
