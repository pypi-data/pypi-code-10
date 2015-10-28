import os
import logging

log = logging.getLogger('chameleon.config')
environment = dict(
    (k[10:], v) for (k, v) in (
        ((j.lower(), x) for (j, x) in os.environ.items()))
    if k.startswith('chameleon_')
)

# Define which values are read as true
TRUE = ('y', 'yes', 't', 'true', 'on', '1')

# If eager parsing is enabled, templates are parsed upon
# instantiation, rather than when first called upon; this mode is
# useful for verifying validity of templates across a project
EAGER_PARSING = environment.pop('eager', 'false')
EAGER_PARSING = EAGER_PARSING.lower() in TRUE

# Debug mode is mostly useful for debugging the template engine
# itself. When enabled, generated source code is written to disk to
# ease step-debugging and some log levels are lowered to increase
# output. Also, the generated source code is available in the
# ``source`` attribute of the template instance if compilation
# succeeded.
DEBUG_MODE = environment.pop('debug', 'false')
DEBUG_MODE = DEBUG_MODE.lower() in TRUE

# If a cache directory is specified, template source code will be
# persisted on disk and reloaded between sessions
path = environment.pop('cache', None)
if path is not None:
    CACHE_DIRECTORY = os.path.abspath(path)
    if not os.path.exists(CACHE_DIRECTORY):
        raise ValueError(
            "Cache directory does not exist: %s." % CACHE_DIRECTORY
            )
    log.info("directory cache: %s." % CACHE_DIRECTORY)
else:
    CACHE_DIRECTORY = None

# When auto-reload is enabled, templates are reloaded on file change.
AUTO_RELOAD = environment.pop('reload', 'false')
AUTO_RELOAD = AUTO_RELOAD.lower() in TRUE

for key in environment:
    log.warning(
        "unknown environment variable set: \"CHAMELEON_%s\"." % key.upper()
    )

# This is the slice length of the expression displayed in the
# formatted exception string
SOURCE_EXPRESSION_MARKER_LENGTH = 60


