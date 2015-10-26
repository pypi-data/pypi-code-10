# coding=utf-8
from __future__ import unicode_literals
from admin_monitoring.admin import admin_monitoring_mixin_factory


class VNP(object):
    """ для отображения числа новых компаний в админке """
    def __init__(self, model, vnp, **kwargs):
        self.model = model
        self.vnp_old = vnp
        self.kwargs = kwargs

    def __unicode__(self):
        # fixes UnicodeDecodeError
        return "%s" % self.__repr__()

    def __repr__(self):
        count = self.model.objects.filter(**self.kwargs).count()
        if count:
            return "%s (%s)" % (self.vnp_old, count)
        else:
            return self.vnp_old


def register(admin_site, model, model_admin=None, filter_kwargs=None, **options):
    """
        пример использования: register(admin.site, Model, ModelAdmin, {"viewed": False})
        таким образом возле названия модели будет подписано число объектов с аттрибутом viewed=False
    """
    if not filter_kwargs:
        filter_kwargs = {}

    AdminMonitoringMixin = admin_monitoring_mixin_factory(**filter_kwargs)

    class ModelAdmin(AdminMonitoringMixin, model_admin):
        pass

    if not hasattr(model._meta, "_verbose_name_plural"):
        model._meta._verbose_name_plural = model._meta.verbose_name_plural
    model._meta.verbose_name_plural = VNP(model, model._meta._verbose_name_plural, **filter_kwargs)

    # class ProxyModel(model):
    #     class Meta:
    #         proxy = True
    #         verbose_name = model._meta.verbose_name
    #         verbose_name_plural = "%s" % VNP(model, model._meta.verbose_name_plural, **filter_kwargs)

    admin_site.register(model, ModelAdmin, **options)
