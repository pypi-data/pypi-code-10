from __future__ import unicode_literals

from ...models import Address

from ..base import Product
from ..dossier import AccommodationDossier


class Accommodation(Product):

    _resource_name = 'accommodations'
    _is_listable = False

    _as_is_fields = ['id', 'href', 'name', 'product_line', 'sku', 'type',
        'sub_type', 'phone_numbers']
    _date_time_fields_utc = ['date_created', 'date_last_modified']
    _model_fields = [('address', Address)]

    @property
    def _model_collection_fields(self):
        from ...models import AccommodationRoom
        return [
           ('rooms', AccommodationRoom), 
        ]

    @property
    def _resource_fields(self):
        return [
           ('accommodation_dossier', AccommodationDossier),
        ]

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

