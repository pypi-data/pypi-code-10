import abc
from expressly.route_responses import BatchInvoiceResponse, BatchCustomerResponse, CustomerResponse


class ProviderBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def customer_register(self, customer) -> bool:
        """
        adds customer to store
        :param customer: expressly.models.Customer
        :return: bool
        """
        return

    @abc.abstractmethod
    def customer_login(self, email) -> bool:
        """
        logs user in based on provided customer_id
        :param customer_id:
        :return: bool
        """
        return

    @abc.abstractmethod
    def customer_add_cart(self, email, product_id=None, coupon_code=None) -> bool:
        """
        add product, and/or coupon to customers' cart - if valid
        :param customer_id:
        :param product_id:
        :param coupon_code:
        :return: bool
        """
        return

    @abc.abstractmethod
    def customer_send_password_email(self, email) -> bool:
        """
        send customer reset/create email
        :param customer_id:
        :return:
        """
        return

    @abc.abstractmethod
    def get_customer(self, email) -> CustomerResponse:
        """
        returns wrapped response of specified customer that conforms to expressly.models.Customer
        :param email:
        :return: Customer
        """
        return

    @abc.abstractmethod
    def get_customer_invoices(self, customers) -> BatchInvoiceResponse:
        """
        returns all associated data with customers, if they exist; data required must conform to object
        :param customers:
        :return: object
        """
        return

    @abc.abstractmethod
    def get_customer_statuses(self, customers) -> BatchCustomerResponse:
        """
        returns all assocaited data for given customers that exist, are pending, or have disabled their account;
        data required must conform to object
        :param customers:
        :return: object
        """
        return
