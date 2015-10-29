from egat.test_runner_helpers import WorkNode
from egat.testset import TestSet
from egat.testset import ExecutionOrder
import pkgutil
import inspect
import itertools
import sys
import os

sys.path.append(os.getcwd())

class TestLoader():
    """A class that does the legwork of importing modules, classes, and functions, 
    finding their tests, and creating WorkNodes from them."""
    @staticmethod
    def get_work_nodes_for_tests(tests):
        """Takes a list of tests in the format:
            {
                'test': 'test_name',
                'configuration': {
                    'var': 'val'
                },
                'environment': {
                    'var': 'val'
                }
            }
            and returns the tests as a list of WorkNode objects."""
        work_nodes = []
        for test in tests:
            work_nodes.extend(TestLoader.get_work_nodes_for_test(test))
        return work_nodes

    @staticmethod
    def get_work_nodes_for_test(test):
        """Takes a test in the format:
            {
                'test': 'test_name',
                'configuration': {
                    'var': 'val'
                },
                'environment': {
                    'var': 'val'
                }
            }
            and returns the tests it contains as a list of WorkNode objects."""
        work_nodes = []
        test_name = test['test']
        conf = test.get('configuration', {})
        env = test.get('environment', {})

        is_module = False
        is_class = False
        is_fn = False
        descriptor_len = len(test_name.split('.' ))
        unrecogized_test_descriptor = "Test descriptor '%s' or one of its dependencies could not be imported as a module, class, or function => " % test_name
        try: is_module = __import__(test_name)
        except ImportError as e:
            if descriptor_len > 1:
                try: is_class = __import__('.'.join(test_name.split('.')[0:-1]))
                except ImportError as e:
                    if descriptor_len > 2:
                        try: is_fn = __import__('.'.join(test_name.split('.')[0:-2]))
                        except ImportError as e:
                            raise ImportError(unrecogized_test_descriptor + e.message)
                    else:
                        raise ImportError(unrecogized_test_descriptor + e.message)
            else:
                raise ImportError(unrecogized_test_descriptor + e.message)

        if is_module:
            load_func = TestLoader.get_work_nodes_from_module_name
        elif is_class:
            load_func = TestLoader.get_work_nodes_from_class_name
        elif is_fn:
            load_func = TestLoader.get_work_nodes_from_function_name
        else:
            raise Exception(
                """Expected fully-qualified module name, class name, or
                function, but got %s""" % (test_name)
            )

        return load_func(test_name, conf, env)

    @staticmethod
    def get_work_nodes_from_module_name(module_name, config={}, env={}):
        """Takes a fully-qualified module/package name, finds all subclasses of 
        TestSet in the module and its submodules and returns a list of those 
        TestSet's tests as WorkNodes."""
        class_names = TestLoader.get_class_names_from_module(module_name)
        classes = filter(TestLoader.is_testset, map(TestLoader.get_class_from_name, class_names))
        get_nodes = lambda cls: TestLoader.get_work_nodes_from_class(cls, config, env)
        return list(itertools.chain(*map(get_nodes, classes)))

    @staticmethod
    def get_work_nodes_from_class_name(name, config={}, env={}):
        """Takes a fully-qualified class name as a string and returns any tests 
        contained in that class as a list of WorkNodes. The specified test should be 
        a subclass of TestSet."""
        class_obj = TestLoader.get_class_from_name(name)
        return TestLoader.get_work_nodes_from_class(class_obj, config, env)

    @staticmethod
    def get_work_nodes_from_class(cls, config={}, env={}):
        """Takes a class object that should be a subclass of TestSet and returns its
        test functions as a list of WorkNodes."""
        work_nodes = []
        # Check to see if this is an ordered or unordered set of tests
        if cls.execution_order == ExecutionOrder.UNORDERED:
            # if it is unordered these test functions are each their own node
            for func in cls.load_tests():
                work_nodes.append(WorkNode(cls, [func], config, env))
        else:
            # if it is ordered then the test functions must all be run together
            work_nodes.append(WorkNode(cls, cls.load_tests(), config, env))
        return work_nodes

    @staticmethod
    def get_work_nodes_from_function_name(full_function_name, config={}, env={}):
        """Takes a fully-qualified function name (i.e. 'pkg.ClassName.function_name') 
        and returns it as a single WorkNode in a list."""
        class_name = '.'.join(full_function_name.split('.')[0:-1])
        function_name = full_function_name.split('.')[-1]

        test_class = TestLoader.get_class_from_name(class_name)
        func = getattr(test_class, function_name)
        return [WorkNode(test_class, [func], config, env)]

    @staticmethod
    def get_class_names_from_module(module_name):
        """Takes a module name like the one passed to the 'import' command and 
        returns a set of all the class names defined in all that module's 
        submodules."""
        class_names = []
        module = __import__(module_name)
        prefix = module_name.split('.')[0] + "."
        original_modname = module_name
        path = getattr(module, '__path__', None)

        if path:
            # module is a package, walk it
            for importer, module_name, ispkg in pkgutil.walk_packages(path, prefix=prefix):
                try:
                    module = importer.find_module(module_name).load_module(module_name)
                    all_classes = [t for t in inspect.getmembers(module, inspect.isclass)]
                    mod_class_names = filter(lambda t: t[1].__module__.startswith(original_modname), all_classes)
                    class_names += [t[1].__module__ + '.' + t[0] for t in mod_class_names]
                except ImportError:
                    pass
        else:
            # module is not a package
            class_names = [t[1].__module__ + '.' + t[0] for t in inspect.getmembers(module, inspect.isclass)]

        return set(class_names)

    @staticmethod
    def get_class_from_name(full_class_name):
        """Takes a fully-qualified class name as a string and returns its class
        object."""
        class_name = full_class_name.split('.')[-1]
        module_name = '.'.join(full_class_name.split('.')[0:-1])
        __import__(module_name)
        root_module = sys.modules[module_name]
        try:
            return getattr(root_module, class_name)
        except AttributeError:
            raise AttributeError("Module '%s' has no attribute '%s'" % (module_name, class_name))

    @staticmethod
    def is_testset(cls):
        """Takes a class object and returns True if it is a subclass of TestSet and
        False otherwise."""
        base_classes = cls.__bases__
        for base in base_classes:
            if base == TestSet or TestLoader.is_testset(base):
                return True
        return False
