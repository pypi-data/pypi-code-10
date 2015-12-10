import os
import abc
import asyncio
from subprocess import Popen, PIPE

import psutil as psutil


class OutOfProcessNodeInstance:
    __metaclass__ = abc.ABCMeta

    def __init__(self, entry_point_script, root_path, *args):
        self.entry_point_script = entry_point_script
        self.root_path = root_path
        self.arguments = ' '.join(args)

        self.ready = False
        self.process = None

    def invoke(self, module_name, *args):
        return self.invoke_export(module_name, None, *args)

    @abc.abstractmethod
    def invoke_export(self, module_name, exported_function_name, *args):
        return

    @asyncio.coroutine
    def initialize_node(self):
        if self.ready is True and self.process is not None:
            return True

        self.before_launch()

        env = os.environ.copy()
        current_path = ''
        if "NODE_PATH" in env:
            current_path = env["NODE_PATH"] + ':'
        env["NODE_PATH"] = current_path + os.path.join(self.root_path, 'node_modules')

        self.process = Popen('node ' + self.entry_point_script + ' ' + self.arguments,
                             shell=True, stdin=PIPE, stdout=PIPE,
                             env=env, cwd=self.root_path)

        result = ''
        while True:
            output = self.process.stdout.readline()
            if self.process.poll() is not None:
                raise RuntimeError(output)
            if output:
                result = output.decode('utf-8').strip()
                if result == '[pynode:Listening]':
                    self.ready = True
                    return True
            asyncio.sleep(0.5)

        raise RuntimeError('Invalid initialization result ' + result)

    def ensure_ready(self):
        loop = asyncio.get_event_loop()
        ready = loop.run_until_complete(self.initialize_node())
        if ready is not True:
            raise RuntimeError('Node instance did not ready correctly')

    def write_input(self, data):
        self.process.stdin.write(bytes(data + '\n', 'utf-8'))
        self.process.stdin.flush()

    def read_output(self):
        output = self.process.stdout.readline()
        if self.process.poll() is not None:
            raise RuntimeError(output)
        return output.decode('utf-8')

    def before_launch(self):
        pass

    def close(self):
        parent = psutil.Process(self.process.pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        psutil.wait_procs(children, timeout=5)
        parent.kill()
        parent.wait(5)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
