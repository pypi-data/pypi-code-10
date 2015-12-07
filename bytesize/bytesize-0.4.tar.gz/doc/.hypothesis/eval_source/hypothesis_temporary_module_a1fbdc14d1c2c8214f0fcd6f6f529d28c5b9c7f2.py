from hypothesis.utils.conventions import not_set

def accept(f):
    def testResults(self, s=not_set, min_val=not_set, binary_units=not_set, exact_value=not_set, max_places=not_set):
        return f(self, s, min_val, binary_units, exact_value, max_places)
    return testResults
