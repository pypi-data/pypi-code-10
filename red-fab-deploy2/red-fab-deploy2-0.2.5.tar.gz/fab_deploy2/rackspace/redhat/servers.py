from fab_deploy2.rackspace import servers as rackspace_servers
from fab_deploy2.operating_systems.redhat.servers import *

class AppServer(rackspace_servers.RSAppServerMixin, AppServer):
    pass

class DBServer(rackspace_servers.RSServerMixin, DBServer):
    pass

class DBSlaveServer(rackspace_servers.RSServerMixin, DBSlaveServer):
    pass

class DevServer(rackspace_servers.RSServerMixin, DevServer):
    pass


AppServer().as_tasks(name="app_server")
DBServer().as_tasks(name="db_server")
DBSlaveServer().as_tasks(name="db_slave_server")
DevServer().as_tasks(name="dev_server")
