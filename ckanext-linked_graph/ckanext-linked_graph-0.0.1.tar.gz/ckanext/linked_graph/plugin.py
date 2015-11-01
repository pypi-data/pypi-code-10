import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class Linked_GraphPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'linked_graph')
	#toolkit.add_resource('fanstatic', 'jqcloud')

    # IRoutes
    def before_map(self, map):
        controller = 'ckanext.linked_graph.controllers:LinkedGraphController'

        map.connect('data-linked-graph', '/linked-graph',
            controller=controller, action='stack_graph')

        return map
