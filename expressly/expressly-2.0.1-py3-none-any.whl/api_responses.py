from schematics.models import Model
from schematics.types import StringType, EmailType, BooleanType

from schematics.types.compound import ModelType
from expressly.models import Customer as CustomerModel
import json


class ApiResponse:
    def __init__(self, status, data, response_cls=None):
        self.status = status
        self.data = data if response_cls is None else response_cls(json.loads(data))


class BannerResponse(Model):
    image_url = StringType(required=True, serialized_name='bannerImageUrl')
    migration_url = StringType(required=True, serialized_name='migrationLink')


class Meta(Model):
    locale = StringType(required=True, max_length=3)
    sender = StringType(required=True)


class Cart(Model):
    product_id = StringType(deserialize_from='productId')
    coupon_code = StringType(deserialize_from='couponCode')


class Customer(Model):
    email = EmailType(required=True)
    data = ModelType(CustomerModel, required=True, deserialize_from='customerData')
    cart = ModelType(Cart)

    class Options:
        serialize_when_none = False


class MigrationCustomerResponse(Model):
    meta = ModelType(Meta, required=True)
    data = ModelType(Customer, required=True)


class MigrationStatusResponse(Model):
    success = BooleanType(required=True)
    message = StringType(required=True, serialized_name='msg')


class PingResponse(Model):
    server_status = StringType(required=True, serialized_name='Server')
    db_status = StringType(required=True, serialized_name='DB Status')
