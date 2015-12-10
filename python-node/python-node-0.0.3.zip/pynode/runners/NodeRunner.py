from Naked.toolshed.shell import muterun_js
from pynode.exceptions import NodeExecutionFailedException
from pynode.runners.Runner import Runner


class NodeRunner(Runner):

    def execute(self, script, *args):
        result = muterun_js('-e "' + script + '"', self.args_to_string(args))
        if result.exitcode == 0:
            return result.stdout.decode('utf-8').strip()
        else:
            raise NodeExecutionFailedException(result.stderr)

    def execute_silent(self, script, *args):
        result = muterun_js('-e "' + script + '"', self.args_to_string(args))
        if result.exitcode == 0:
            return True
        else:
            raise NodeExecutionFailedException(result.stderr)

    def execute_script(self, script_path, *args):
        result = muterun_js(script_path, self.args_to_string(args))
        if result.exitcode == 0:
            return result.stdout.decode('utf-8').strip()
        else:
            raise NodeExecutionFailedException(result.stderr)

    def execute_script_silent(self, script_path, *args):
        result = muterun_js(script_path, self.args_to_string(args))
        if result.exitcode == 0:
            return True
        else:
            raise NodeExecutionFailedException(result.stderr)

    def invoke(self, module_name, *args):
        pass

    def invoke_export(self, module_name, function_name, *args):
        pass
