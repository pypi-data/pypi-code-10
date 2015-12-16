from schematics.types import EmailType, StringType
from schematics.types.compound import ListType, ModelType
from expressly.models import JsonModel, Invoice, FieldValue, Customer as CustomerModel


class Meta(JsonModel):
    locale = StringType()
    issuer_data = ListType(ModelType(FieldValue), serialized_name='issuerData')

    class Options:
        serialize_when_none = False


class Customer(JsonModel):
    email = EmailType(required=True)
    user_reference = StringType(required=True, serialized_name='userReference')
    customer_data = ModelType(CustomerModel, required=True, serialized_name='customerData')


class PingResponse:
    def __str__(self):
        return '{"expressly": "Stuff is happening!"}'


class RegisteredResponse:
    def __str__(self):
        return '{"registered": true}'


class CustomerResponse(JsonModel):
    meta = ModelType(Meta)
    data = ModelType(Customer, required=True)

    class Options:
        serialize_when_none = False


class BatchCustomerResponse(JsonModel):
    existing = ListType(EmailType)
    deleted = ListType(EmailType)
    pending = ListType(EmailType)

    class Options:
        serialize_when_none = False


class BatchInvoiceResponse(JsonModel):
    invoices = ListType(ModelType(Invoice))

    class Options:
        serialize_when_none = False
