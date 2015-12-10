from Naked.toolshed.shell import muterun
from pynode.exceptions import NodeExecutionFailedException
from pynode.runners.Runner import Runner


class BabelRunner(Runner):

    def __init__(self, ignore=None, extensions=None, presets=None, plugins=None):
        babel_arguments = ''
        if ignore is not None:
            babel_arguments += '-i ' + ignore + ' '
        if extensions is not None:
            babel_arguments += '-x ' + extensions + ' '
        if presets is not None:
            babel_arguments += '--presets ' + presets + ' '
        if plugins is not None:
            babel_arguments += '--plugins ' + plugins + ' '
        self.babel_arguments = babel_arguments

    def execute_babel_node(self, expression_or_path, arguments):
        try:
            if len(arguments) > 0:
                js_command = 'babel-node ' + self.babel_arguments + expression_or_path + ' ' + arguments
            else:
                js_command = 'babel-node ' + self.babel_arguments + expression_or_path
            return muterun(js_command)  # return result of execute_babel_node() of node.js file
        except Exception as e:
            raise e

    def execute(self, script, *args):
        result = self.execute_babel_node('-e "' + script + '"', self.args_to_string(args))
        if result.exitcode == 0:
            return result.stdout.decode('utf-8').strip()
        else:
            raise NodeExecutionFailedException(result.stderr)

    def execute_silent(self, script, *args):
        result = self.execute_babel_node('-e "' + script + '"', self.args_to_string(args))
        if result.exitcode == 0:
            return True
        else:
            raise NodeExecutionFailedException(result.stderr)

    def execute_script(self, script_path, *args):
        result = self.execute_babel_node(script_path, self.args_to_string(args))
        if result.exitcode == 0:
            return result.stdout.decode('utf-8').strip()
        else:
            raise NodeExecutionFailedException(result.stderr)

    def execute_script_silent(self, script_path, *args):
        result = self.execute_babel_node(script_path, self.args_to_string(args))
        if result.exitcode == 0:
            return True
        else:
            raise NodeExecutionFailedException(result.stderr)
