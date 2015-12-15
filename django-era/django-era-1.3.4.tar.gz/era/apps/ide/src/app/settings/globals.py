from itertools import chain
from era import _
from era.apps.user.settings import *
from era.settings import *
from era.utils.translation import ru

MODULES += ['users']
ERA_APPS = ['era.apps.user']
DJANGO_APPS = []
INSTALLED_APPS +=  DJANGO_APPS + ERA_APPS + MODULES
BOWER_INSTALLED_APPS += []

TITLE = _('Gig4Life')
MAIN_MENU = ['users']
USER_ROLES = [_('developer'), _('admin'), _('member')]

try:from .locals import *
except ImportError: pass

if DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']
