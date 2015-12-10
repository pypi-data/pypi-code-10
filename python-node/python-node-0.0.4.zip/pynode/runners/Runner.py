import abc


class Runner(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def args_to_string(args):
        result = ''
        for count, arg in enumerate(args):
            result += ' ' + arg
        return result

    @abc.abstractmethod
    def execute(self, script, *args):
        """Evaluate inline JavaScript and return the result"""
        return

    @abc.abstractmethod
    def execute_silent(self, script, *args):
        """Evaluate inline JavaScript and return True if it exitted successfully"""
        return

    @abc.abstractmethod
    def execute_script(self, script_path, *args):
        """Evaluate a JavaScript file and return the result"""
        return

    @abc.abstractmethod
    def execute_script_silent(self, script_path, *args):
        """Evaluate a JavaScript file and return True if it exitted successfully"""
        return

    @abc.abstractmethod
    def invoke(self, module_name, *args):
        """Import and invoke a node module"""
        return

    @abc.abstractmethod
    def invoke_export(self, module_name, function_name, *args):
        """Import and invoke a function from a node module"""
        return
