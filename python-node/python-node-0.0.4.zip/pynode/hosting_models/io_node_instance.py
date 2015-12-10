import json
import os
from .out_of_process_node_instance import OutOfProcessNodeInstance

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content', 'node', 'entrypoint-stream.js')


class IONodeInstance(OutOfProcessNodeInstance):
    def __init__(self, root_path, *args, **kwargs):
        super().__init__(script_path, root_path, *args, **kwargs)

    def invoke_export(self, module_name, exported_function_name, *args):
        self.ensure_ready()

        payload_json = json.dumps({
            'moduleName': module_name,
            'exportedFunctionName': exported_function_name,
            'args': args
        })
        self.write_input('\ninvoke:' + payload_json)
        response = self.read_output()
        try:
            return json.loads(response)
        except ValueError:
            return response.strip()
