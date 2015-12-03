from django.conf import settings


MODEL_TREE = getattr(settings, 'MOJO_MODEL_TREE', 'navigation.Tree')
