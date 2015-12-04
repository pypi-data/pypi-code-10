from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.conf import settings

# List with constant variables.
ACL_CODE_PREFIX = getattr(settings, 'ACL_CODE_PREFIX', 'view.')
ACL_NAME_PREFIX = getattr(settings, 'ACL_NAME_PREFIX', 'ACL ')

DEFAULT_EXCLUDED_VIEWS = ('django.*',)
ACL_EXCLUDED_VIEWS = getattr(settings, 'ACL_EXCLUDED_VIEWS', ()) + DEFAULT_EXCLUDED_VIEWS
ACL_ALLOWED_VIEWS = getattr(settings, 'ACL_ALLOWED_VIEWS', ())


def generate_permissions(urlpatterns, permissions={}):
    """Generate names for permissions."""
    for pattern in urlpatterns:
        if isinstance(pattern, urlresolvers.RegexURLPattern):
            perm = generate_perm_name(pattern.callback)
            if is_allowed_view(perm) and perm not in permissions:
                permissions[ACL_CODE_PREFIX + perm] = ACL_NAME_PREFIX + perm
        elif isinstance(pattern, urlresolvers.RegexURLResolver):
            generate_permissions(pattern.url_patterns, permissions)
    return permissions


def generate_perm_name(func):
    """Generate permission name from callback function."""
    return '.'.join((func and func.__module__ or '',
                     func and func.__name__ or ''))


def is_allowed_view(perm):
    """Check if permission is in acl list."""

    # Check if permission is in excluded list
    for view in ACL_EXCLUDED_VIEWS:
        module, separator, view_name = view.partition('*')
        if view and perm.startswith(module):
            return False

    # Check if permission is in acl list
    for view in ACL_ALLOWED_VIEWS:
        module, separator, view_name = view.partition('*')
        if separator and not module and not view_name:
            return True
        elif separator and module and perm.startswith(module):
            return True
        elif separator and view_name and perm.endswith(view_name):
            return True
        elif not separator and view == perm:
            return True
    return False

def refresh_permissions(permissions):
    """Refresh permission:
       Remove deprecated permissions,
       Add generated permissions."""
    available_permissions = [x.codename for x in
                             Permission.objects.filter(
                                 codename__startswith=ACL_CODE_PREFIX)]
    active_permissions = permissions.keys()

    perms_to_add = set(active_permissions) - set(available_permissions)
    perms_to_remove = set(available_permissions) - set(active_permissions)

    # Remove deprecated permissions
    for codename in perms_to_remove:
        Permission.objects.filter(codename=codename).delete()

    # Add generated permissions
    ct = ContentType.objects.get_for_model(model=auth_models.User)
    for codename in perms_to_add:
        Permission.objects.get_or_create(codename=codename,
                                         name=permissions[codename],
                                         content_type=ct)
