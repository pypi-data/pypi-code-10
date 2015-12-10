import json
import os
import requests
from .out_of_process_node_instance import OutOfProcessNodeInstance

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content', 'node', 'entrypoint-http.js')


class HttpNodeInstance(OutOfProcessNodeInstance):
    def __init__(self, root_path, *args, **kwargs):
        if 'port' in kwargs:
            self.port = kwargs["port"]
        else:
            self.port = 8080
        super().__init__(script_path, root_path, str(self.port))

    def invoke_export(self, module_name, exported_function_name, *args):
        self.ensure_ready()

        try:
            payload_json = json.dumps({
                'moduleName': module_name,
                'exportedFunctionName': exported_function_name,
                'args': args
            })
            response = requests.post('http://localhost:' + str(self.port), data=payload_json)
            try:
                return json.loads(response.text)
            except ValueError:
                return response.text
        except Exception as exception:
            self.process.terminate()
            raise exception
