class Apis:

    def iodoc_from_swagger(self, public_domain, external_api_definition):
        iodoc = {}
        iodoc['name'] = external_api_definition['info']['title']
        iodoc['title'] = external_api_definition['info']['title']
        iodoc['version'] = external_api_definition['info']['version']
        iodoc['description'] = external_api_definition['info']['description']
        iodoc['protocol'] = 'rest'
        iodoc['basePath'] = external_api_definition['schemes'][0] + '://' + external_api_definition['basePath'] + external_api_definition['basePath'] 

        iodoc['resources'] = {}
        for path in external_api_definition['paths']:
            iodoc['resources'][path] = {'methods': {}}
            for http_method in external_api_definition['paths'][path]:
                method = external_api_definition['paths'][path][http_method]
                iodoc['resources'][path]['methods'][method['operationId']] = {'path': path, 'httpMethod': http_method.upper(), 'description': method['description'], 'parameters': {}}
                for parameter in method['parameters']:
                    #'type': parameter['type']  , 'description': parameter['description']
                    iodoc_parameter = {'required': parameter['required'], 'location': parameter['in']}
                    iodoc['resources'][path]['methods'][method['operationId']]['parameters'][parameter['name']] = iodoc_parameter

        return iodoc


    def from_swagger(self, public_domain, external_api_definition):
        api = {}
        api['name'] = external_api_definition['info']['title']
        api['version'] = external_api_definition['info']['version']
        api['description'] = external_api_definition['info']['description']

        api['endpoints'] = []

        for path in external_api_definition['paths']:
            endpoint = {}
            endpoint['name'] = path.replace('/', ' ').replace('{', ' ').replace('}', ' ').strip()
            endpoint['requestPathAlias'] = external_api_definition['basePath'] + path
            endpoint['targetRequestPath'] = external_api_definition['basePath'] + path

            if external_api_definition['schemes'][0] == 'https':
                endpoint['inboundSslRequired'] = True
            else:
                endpoint['inboundSslRequired'] = False

            endpoint['publicDomains'] = [{'address': public_domain}]
            endpoint['systemDomains'] = [{'address': external_api_definition['host']}]

            endpoint['supportedHttpMethods'] = []
            for http_method in external_api_definition['paths'][path]:
                endpoint['supportedHttpMethods'].append(http_method)

            api['endpoints'].append(endpoint)

        return api

    def from_raml(self, external_api_definition):		
        api = {}

        return api

    def to_swagger(self, api_definition):
        external_api_definition = {}

        return external_api_definition

    def to_raml(self, api_definition):        
        external_api_definition = {}

        return external_api_definition
