# operations of env vars

class Operation(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def identify(self, inspector):
        raise NotImplementedError

class Set(Operation):
    
    def identify(self, inspector):
        return inspector.onSet(self)


class Prepend(Operation):
    
    def identify(self, inspector):
        return inspector.onPrepend(self)


class Append(Operation):
    
    def identify(self, inspector):
        return inspector.onAppend(self)
