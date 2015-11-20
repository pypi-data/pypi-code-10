from django.db import models

from parent_swap.swap import BaseMapping, BaseModel


class SimpleObject(BaseModel):
    """
    Basic object inheriting from an abstract base class
    """
    foo = models.CharField(max_length=256)

    class Mapping(BaseMapping):
        pass
