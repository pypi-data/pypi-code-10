'''
This module contain's a specialised ShellTask, optimized for executing shell
commands
'''

import logging
import luigi
import sciluigi.task

# ========================================================================

def new_shelltask(name, command_pattern, workflow_task, **kwargs):
    kwargs['command_pattern'] = command_pattern
    return sciluigi.task.new_task(name, ShellTask, workflow_task, **kwargs)

# ========================================================================

class ShellTask(sciluigi.task.Task):
    command_pattern = luigi.Parameter()

    def requires(self):
        upstream_tasks = []
        if hasattr(self, 'inports'):
            for portname, inport in self.inports.iteritems():
                if type(inport) is dict:
                    upstream_tasks.append(inport['upstream']['task'])
        return upstream_tasks

    def output(self):
        cmd = self._replace_inputs(self.cmd)
        ms = self._find_outputs(cmd)
        outputs = {m[1]: luigi.LocalTarget(m[3]) for m in ms}
        return outputs

    def run(self):
        cmd = self._replace_inputs(self.cmd)
        ms = self._find_outputs(cmd)
        for m in ms:
            cmd = cmd.replace(m[0], self.output()[m[1]].path)
        print("****** NOW RUNNING COMMAND ******: " + cmd)
        # Remove any trailing comments in the line
        cmd = re.sub('(\ )?\#.*$', '', cmd)
        print commands.getstatusoutput(cmd)

        if self.command == '':
            raise Exception('Command is not set for ShellTask!')
        else:
            self.ex(self.command)

# ========================================================================
