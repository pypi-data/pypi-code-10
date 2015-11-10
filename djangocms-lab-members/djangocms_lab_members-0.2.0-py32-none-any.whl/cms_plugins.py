# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cms_lab_members.models import ScientistPluginModel

class ScientistPlugin(CMSPluginBase):
    model = ScientistPluginModel
    module = "Lab Plugins"
    name = _("Scientist Plugin")
    render_template = "cms_lab_members/plugin.html"

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

plugin_pool.register_plugin(ScientistPlugin)
