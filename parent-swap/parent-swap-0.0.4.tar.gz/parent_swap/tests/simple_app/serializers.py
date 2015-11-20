from parent_swap.swap import BaseSerializer

from .models import SimpleObject


class SimpleObjectSerializer(BaseSerializer):
    """
    Basic object inheriting from a configurable BaseSerializer
    """
    class Meta:
        model = SimpleObject
