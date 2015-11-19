TEMPLATE_PATH = '/root/coreInit/coreinit/templates/'

# Module name with Logger class. E.g. coreinit.logger.syslog
DEFAULT_LOGGER = 'coreinit.logger.syslog_driver'

DEFAULT_DB = 'coreinit.db.drivers.redis_driver'

CACHE_URL = 'localhost'

import os
import imp
import sys

if 'COREINIT_CONFIG' in os.environ:
    ext_config = imp.load_source('x', os.environ['COREINIT_CONFIG'])
    for variable in dir(ext_config):
        print "Overriding variable %s" % variable
        setattr(sys.modules[__name__], variable, getattr(ext_config, variable))
else:
    print "No additional configuration"
