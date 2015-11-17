from taiga.base.api.permissions import (TaigaResourcePermission, IsProjectOwner,
                                        AllowAny)


class IframePluginPermissions(TaigaResourcePermission):
    retrieve_perms = IsProjectOwner()
    create_perms = IsProjectOwner()
    update_perms = IsProjectOwner()
    destroy_perms = IsProjectOwner()
    list_perms = AllowAny()
