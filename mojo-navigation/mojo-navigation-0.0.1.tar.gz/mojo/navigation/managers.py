from django.contrib.auth.models import Permission
from django.db.models import Q

from mptt.managers import TreeManager


class ItemManager(TreeManager):
    """
    Specific manager for mojo.navigation Item models.
    """
    def for_slug(self, slug):
        """
        Filters items for a specific tree by its slug.

        :param slug: Slugified string.
        :type slug: str

        Usage exemple::

            tree_items = Item.objects.for_slug('slug_exemple')
        """
        queryset = super(ItemManager, self).get_queryset()
        return queryset.filter(slug=slug).get_descendants(include_self=True)

    def for_user(self, user):
        """
        Filters items for a specific user and his permissions.

        :param user: Django user object instance.
        :type user: obj

        Usage exemple::

            tree_items = Item.objects.for_user(request.user)
        """
        queryset = super(ItemManager, self).get_queryset()
        # if user is superuser, do not filter anything.
        if user.is_superuser:
            return queryset
        # if user is not authenticated remove tree items only set for authenticated users.
        if not user.is_active:
            queryset = queryset.exclude(access_loggedin=True)
        # then add items that user has group access to.
        groups = user.groups.all()
        queryset = queryset.filter(Q(access_group=None) | Q(access_group__in=groups))
        # then add items that user has permission access to.
        group_permissions = Permission.objects.filter(group__in=groups)
        queryset = queryset.filter(Q(access_permissions=None)
                                   | Q(access_permissions__in=user.user_permissions.all())
                                   | Q(access_permissions__in=group_permissions))
        return queryset
