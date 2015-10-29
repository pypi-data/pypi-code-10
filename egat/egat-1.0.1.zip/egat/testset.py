import inspect

class ExecutionOrder():
    """An Enum that is used to designate whether a TestSet's tests
    need to be run sequentially or can be run in any order."""
    UNORDERED = 0
    SEQUENTIAL = 1

class TestSet():
    """A very general class that represents an arbitrary set of tests. By default 
    each test in a TestSet should be a instance method that begins with the string 
    'test', however the 'load_tests' method may be overridden to modify this 
    behavior. A TestSet may also include 'setup' and 'teardown' methods, called 
    before the tests in the set start and after they are finished, respectively."""

    execution_order = ExecutionOrder.UNORDERED
    configuration = None
    environment = None

    @classmethod
    def load_tests(cls):
        """A method used by the test runner to obtain the list of test functions 
        this TestSet defines. The list returned should be a list of function 
        objects which are instance methods available to this class. The order of the
        tests returned from the TestSet base class is undefined."""

        # Find all methods prefixed with the testMethodPrefix
        testMethodPrefix = "test"
        test_functions = []
        testFnNames = filter(lambda n,p=testMethodPrefix: 
                             n[:len(p)] == p, dir(cls))
        members = inspect.getmembers(cls, predicate=inspect.ismethod)
        for function_name, function in members:
            if function_name in testFnNames:
                test_functions.append(function)

        # Recur on superclasses to get their test methods as well
        for baseclass in cls.__bases__:
            for function in baseclass.load_tests():
                if function.__name__ not in testFnNames:  
                    testFnNames.append(testFnName)        
                    test_functions.append(function)

        return test_functions 

    @classmethod
    def validate(cls, boolean_expression, error_message=""):
        """Asserts that the condition passed into 'boolean_expression' is true and raises the
        error message specified by 'error_message' if it is false."""
        assert boolean_expression, error_message
        
class SequentialTestSet(TestSet):
    """A TestSet whose tests are called in the order they are written (by line 
    number). In addition the setup() and teardown() are called before the first and 
    last test only, instead of after every test method."""
    execution_order = ExecutionOrder.SEQUENTIAL

    @classmethod
    def load_tests(cls):
        """Like the load_test method in TestSet but sorts the test methods by their 
        line number. The youngest subclass has it's methods run first, and each 
        ancestor's test methods are called after it's child's."""
        ln = lambda f: f.im_func.func_code.co_firstlineno
        lncmp = lambda a, b: cmp(ln(a), ln(b))
        # Find all methods prefixed with the testMethodPrefix
        testMethodPrefix = "test"
        test_functions = []
        testFnNames = filter(lambda n,p=testMethodPrefix: 
                             n[:len(p)] == p, dir(cls))
        members = inspect.getmembers(cls, predicate=inspect.ismethod)
        for function_name, function in members:
            if function_name in testFnNames:
                test_functions.append(function)
        test_functions.sort(lncmp)

        # Recur on superclasses to get their test methods as well
        for baseclass in cls.__bases__:
            superclass_functions = [] 
            for function in baseclass.load_tests():
                if function.__name__ not in testFnNames:  
                    testFnNames.append(testFnName)        
                    superclass_functions.append(function)
            # sort the superclasses functions and add them to the end of the 
            # test_functions list
            superclass_functions.sort(lncmp)
            test_functions += superclass_functions

        return test_functions 

class UnorderedTestSet(TestSet):
    """A TestSet whose tests can be called in any order. Prefer this subclass over
    the TestSet superclass, as the TestSet's ExecutionOrder is not defined."""
    execution_order = ExecutionOrder.UNORDERED
