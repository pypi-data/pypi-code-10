from faker import Faker
from .provider import Provider, ProviderList, ProviderAccessor  # flake8: noqa
from .common import Common, Control, WrappedPackages, WrappedFuncs


DefaultProviders = ProviderList([Common(), Control(), WrappedPackages(), WrappedFuncs(), Faker()])
