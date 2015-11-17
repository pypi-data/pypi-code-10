from __future__ import (absolute_import)

from logging import getLogger
from pkg_resources import require

logger = getLogger(__name__)

__version__ = require("filter_variants")[0].version

from .log import init_log, LEVELS
