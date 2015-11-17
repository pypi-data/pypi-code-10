from django.apps import AppConfig

from taiga.contrib_routers import router

from .api import IframePluginViewSet

# register route
router.register(r"iframe", IframePluginViewSet, base_name="iframe")


class IframePluginAppConfig(AppConfig):
    name = "taiga_plugin_iframe"
    verbose_name = "Taiga Iframe Plugin"
