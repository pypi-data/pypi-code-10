import importlib
import logging

from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_q.models import Task


@receiver(post_save, sender=Task)
def call_hook(sender, instance, **kwargs):
    if instance.hook:
        logger = logging.getLogger('django-q')
        f = instance.hook
        if not callable(f):
            try:
                module, func = f.rsplit('.', 1)
                m = importlib.import_module(module)
                f = getattr(m, func)
            except (ValueError, ImportError, AttributeError):
                logger.error(_('malformed return hook \'{}\' for [{}]').format(instance.hook, instance.name))
                return
        try:
            f(instance)
        except Exception as e:
            logger.error(_('return hook {} failed on [{}] because {}').format(instance.hook, instance.name, e))
