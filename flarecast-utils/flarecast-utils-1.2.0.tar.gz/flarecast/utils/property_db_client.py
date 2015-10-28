import requests
from flarecast.utils.rest_exception import RestException


class PropertyDBClient(object):
    __INSERT_PROPERTY_GROUP_URL = '/%s/property-group/'
    __INSERT_PROPERTY_URL = '/property/'
    __INSERT_PROPERTY_AS_PROVENANCE_URL = '/%s/property/'
    __INSERT_PROVENANCE_URL = '/provenance/'
    __INSERT_PROPERTY_GROUP_TYPE_URL = '/%s/property-group-type/'
    __INSERT_LINK_URL = '/link/'
    __DELETE_PROPERTY_GROUP_URL = '/%s/property-group/%s'
    __QUERY_PROPERTY_GROUPS = '/query/%s/%s'

    def __init__(self, property_db_url):
        self.property_db_url = property_db_url

    # -- query --
    def query(self, provenance, sirql_arguments=''):
        if sirql_arguments != '':
            sirql_arguments = '?' + sirql_arguments

        url = self.property_db_url + self.__QUERY_PROPERTY_GROUPS % (
            provenance,
            sirql_arguments)

        return self.__get_request(url)

    # -- delete --

    def delete_property_group(self, provenance, sirql_arguments=''):
        if sirql_arguments != '':
            sirql_arguments = '?' + sirql_arguments

        url = self.property_db_url + self.__DELETE_PROPERTY_GROUP_URL % (
            provenance,
            sirql_arguments)
        return self.__delete_request(url)

    # -- inserts --

    def insert_property_groups(self, provenance, property_groups):
        url = self.property_db_url + self.__INSERT_PROPERTY_GROUP_URL % (
            provenance)
        return self.__post_request(url, property_groups)

    def insert_properties(self, properties):
        url = self.property_db_url + self.__INSERT_PROPERTY_URL
        return self.__post_request(url, properties)

    # todo: name this properly
    def insert_properties_as_provenance(self, provenance, properties):
        url = self.property_db_url + \
              self.__INSERT_PROPERTY_AS_PROVENANCE_URL % \
              (provenance)
        return self.__post_request(url, properties)

    def insert_provenances(self, provenance_list):
        url = self.property_db_url + self.__INSERT_PROVENANCE_URL
        return self.__post_request(url, provenance_list)

    def insert_links(self, link_list):
        url = self.property_db_url + self.__INSERT_LINK_URL
        return self.__post_request(url, link_list)

    # -- add --

    def add_provenance(self, name):
        return self.insert_provenances([name])

    def add_property_group(self, provenance, time_start, **attributes):
        group = {'time_start': time_start}
        group.update(attributes)

        return self.insert_property_groups(provenance, [group])

    def add_properties(self, property_group_fcid, provenance=None, **properties):
        props = {property_group_fcid: properties}

        if provenance is None:
            return self.insert_properties(props)

        return self.insert_properties_as_provenance(provenance, props)

    def add_link(self, source, target, link_type, description):
        link = {'source': source,
                'target': target,
                'type': link_type,
                'description': description}
        return self.insert_links([link])

    # -- get --

    def get_provenances(self):
        url = self.property_db_url + self.__INSERT_PROVENANCE_URL
        return self.__get_request(url)

    @staticmethod
    def __post_request(url, payload):
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, json=payload, headers=headers)

        if r.status_code != 200:
            raise RestException(r)

        return r.json()

    @staticmethod
    def __delete_request(url):
        r = requests.delete(url)

        if r.status_code != 200:
            raise RestException(r)

        return r.text

    @staticmethod
    def __get_request(url):
        r = requests.get(url)

        if r.status_code != 200:
            raise RestException(r)

        return r.json()
