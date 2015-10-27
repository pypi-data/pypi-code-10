from django.dispatch import receiver
from django.db.models.signals import pre_delete
from cms.models.pagemodel import Page
from cms.signals import post_publish, post_unpublish
from .utils import export_page, delete_exported_page
from . import app_settings


if app_settings.AUTO_EXPORT:
    @receiver(post_unpublish)
    @receiver(pre_delete, sender=Page)
    def delete_handle(sender, **kwargs):
        delete_exported_page(kwargs['instance'], language=kwargs['language'])

    @receiver(post_publish)
    def export_handler(sender, **kwargs):
        export_page(kwargs['instance'], language=kwargs['language'])
