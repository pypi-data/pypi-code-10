import simplejson as json

from decimal import Decimal, ROUND_UP
from schematics.models import Model
from schematics.types import StringType, IntType, DateType, FloatType, EmailType, DecimalType
from schematics.types.compound import ListType, ModelType
from schematics.types.serializable import serializable
from expressly.resources import CountryCodes

DateTimeRegex = r'\A([\+-]?\d{4}(?!\d{2}\b))((-?)((0[1-9]|1[0-2])(\3([12]\d|0[1-9]|3[01]))?|W([0-4]\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\d|[12]\d{2}|3([0-5]\d|6[1-6])))([T\s]((([01]\d|2[0-3])((:?)[0-5]\d)?|24\:?00)([\.,]\d+(?!:))?)?(\17[0-5]\d([\.,]\d+)?)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?)?)?\Z'


class JsonModel(Model):
    def __str__(self):
        return json.dumps(self.serialize())


class FieldValue(JsonModel):
    field = StringType(required=True)
    value = StringType(required=True)


class Email(JsonModel):
    email = EmailType(required=True)
    alias = StringType(required=True)


class Phone(JsonModel):
    type = StringType(required=True)
    number = StringType(required=True)
    country_code = StringType(required=True, serialized_name='countryCode', min_length=2, max_length=2)


class Address(JsonModel):
    first_name = StringType(required=True, serialized_name='firstName')
    last_name = StringType(required=True, serialized_name='lastName')
    address1 = StringType(required=True)
    address2 = StringType()
    city = StringType()
    company_name = StringType(serialized_name='companyName')
    zip = StringType()
    phone = IntType()
    alias = StringType(required=True, default='primary')
    state = StringType(serialized_name='stateProvince')
    country = StringType(required=True, choices=CountryCodes.codes)

    class Options:
        serialize_when_none = False


class Customer(JsonModel):
    first_name = StringType(required=True, serialized_name='firstName')
    last_name = StringType(required=True, serialized_name='lastName')
    gender = StringType(choices=['M', 'F'])
    billing_address = IntType(serialized_name='billingAddress')
    shipping_address = IntType(serialized_name='shippingAddress')
    company = StringType()
    dob = DateType()
    tax_number = StringType(serialized_name='taxNumber')
    online_presence = ListType(ModelType(FieldValue), serialized_name='onlinePresence')
    # cannot be DateTimeType; timezone offset is broken for current schematics version (doesn't accept colon separator)
    date_updated = StringType(serialized_name='dateUpdated', regex=DateTimeRegex)
    date_last_order = StringType(serialized_name='dateLastOrder', regex=DateTimeRegex)
    number_ordered = IntType(serialized_name='numberOrdered')
    emails = ListType(ModelType(Email))
    phones = ListType(ModelType(Phone))
    addresses = ListType(ModelType(Address))

    class Options:
        serialize_when_none = False


class Order(JsonModel):
    id = StringType()
    date = StringType(required=True, regex=DateTimeRegex)
    item_count = IntType(min_value=1, required=True, serialized_name='itemCount')
    coupon = StringType()
    currency = StringType()
    total = DecimalType(required=True, serialized_name='preTaxTotal')
    tax = DecimalType(required=True)

    @serializable(serialized_name='postTaxTotal')
    def post_tax_total(self):
        return Decimal(self.total + self.tax).quantize(Decimal('.01'), rounding=ROUND_UP)

    class Options:
        serialize_when_none = False


class Invoice(JsonModel):
    email = EmailType(required=True)
    orders = ListType(ModelType(Order))

    @serializable(serialized_name='orderCount')
    def order_count(self):
        if self.orders is None:
            return 0
        return len(self.orders)

    @serializable(serialized_name='preTaxTotal')
    def total(self):
        if self.orders is None:
            return Decimal(0).quantize(Decimal('.01'))
        return Decimal(sum(o.total for o in self.orders)).quantize(Decimal('.01'), rounding=ROUND_UP)

    @serializable(serialized_name='tax')
    def tax(self):
        if self.orders is None:
            return Decimal(0).quantize(Decimal('.01'))
        return Decimal(sum(o.tax for o in self.orders)).quantize(Decimal('.01'), rounding=ROUND_UP)

    @serializable(serialized_name='postTaxTotal')
    def post_tax_total(self):
        return Decimal(self.total + self.tax).quantize(Decimal('.01'), rounding=ROUND_UP)

    class Options:
        serialize_when_none = False
