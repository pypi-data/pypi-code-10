class SharedResource():
    """An abstract class that represents some resource shared by more than one 
    test. A SharedResource provides a decorator that should be used to designate 
    functions that share the same resource. This designation allow the TestRunner 
    to deduce which tests can be run simultaneously and which cannot. The decorator 
    appends the class name to the 'resources' attribute of the function."""

    @classmethod
    def decorator(cls, func_or_class):
        """A decorator method that adds this class to a 'resources' list on the 
        decorated object."""
        resources = getattr(func_or_class, 'resources', [])
        resources.append(cls)
        func_or_class.resources = resources
        return func_or_class
