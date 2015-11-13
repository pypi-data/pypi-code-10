from hypothesis.utils.conventions import not_set

def accept(f):
    def testExactness(self, n=not_set, e=not_set):
        return f(self, n, e)
    return testExactness
