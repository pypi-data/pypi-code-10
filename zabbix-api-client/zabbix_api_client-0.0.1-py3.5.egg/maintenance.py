from zabbix_api_client.client import Client

SCHEMA = {
    'type': 'object',
    'propertes': {
        'maintenanceid': {
            'type': 'string'
        },
        'name': {
            'type': 'string'
        },
        'active_since': {
            'type': 'string'
        },
        'active_till': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'maintenance_type': {
            'type': 'string'
        },
        'groupids': {
            'type': 'array',
            'items': {
                'type': 'integer'
            }
        },
        'hostids': {
            'type': 'array',
            'items': {
                'type': 'integer'
            }
        },
        'timeperiods': {
            'type': 'array',
            'items': {
                'type': 'integer'
            }
        }
    },
}


class Maintenance(Client):
    """Zabbix Maintenance API"""

    def __init__(self, **kwargs):
        super(Maintenance, self).__init__(**kwargs)

    def create(self, params={}):
        return self.request('maintenance.create', params)

    def delete(self, params={}):
        return self.request('maintenance.delete', params)

    def exists(self, params={}):
        return self.request('maintenance.exists', params)

    def get(self, params={}):
        self.validate(params, SCHEMA)
        params.update({
            'output': 'extend',
            'selectHosts': 'extend',
            'selectGroups': 'extend',
            'selectTimeperiods': 'extend'
        })
        return self.request('maintenance.get', params)

    def update(self, params={}):
        update_schema = {
            'required': [
                'name',
                'maintenanceid',
                'active_since',
                'active_till'
            ]
        }
        update_schema.update(SCHEMA)
        self.validate(params, update_schema)
        params['active_since'] = self.unixtime(params['active_since'])
        params['active_till'] = self.unixtime(params['active_till'])
        get_res = self.get({
            'maintenanceids': [params['maintenanceid']]
        })[0]
        for key in ('timeperiods', 'hosts', 'groups'):
            if key in get_res:
                params[key] = get_res[key]
        params['timeperiods'] = get_res['timeperiods']
        if 'hosts' in get_res and len(get_res['hosts']) > 0:
            params['hostids'] = [get_res['hosts'][0]['hostid']]
        if 'groups' in get_res and len(get_res['groups']) > 0:
            params['groupids'] = [get_res['groups'][0]['groupid']]
        return self.request('maintenance.update', params)
