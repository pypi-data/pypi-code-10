from django.contrib.auth.models import Permission
from django.http import HttpResponseForbidden

from .utils import generate_perm_name, ACL_CODE_PREFIX


class CustomViewProcessMiddleware(object):
    """Middleware class for checking user access to django view."""

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        # User is Anonymous don't check any permission for access.
        if user.is_authenticated():
            view_perm = ACL_CODE_PREFIX + generate_perm_name(view_func)
            perm = Permission.objects.filter(codename=view_perm)
            # Perm for view exists in db and user doesn't have access
            # block and send 403 error
            if perm and not perm.filter(user=user):
                return HttpResponseForbidden()
        return view_func(request, *view_args, **view_kwargs)
