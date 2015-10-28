# coding=utf-8

from __future__ import print_function
try:
    from string import maketrans
except ImportError:  # Python 3
    maketrans = str.maketrans
    basestring = str
import re


PHONE_REGEX = re.compile(r'^(\+\d+)\.(\d)(\d+)$')


def camel_to_snake(string):
    """
    Converts a camelCaseString to a snake_case_string.

    >>> camel_to_snake("fooBarBaz")
    'foo_bar_baz'
    """
    return re.sub('([A-Z]+)', r'_\1', string).lower()


def snake_to_camel(value):
    """
    Converts a snake_case_string to a camelCaseString.

    >>> snake_to_camel("foo_bar_baz")
    'fooBarBaz'
    """
    camel = "".join(word.title() for word in value.split("_"))
    return value[:1].lower() + camel[1:]


def parse_phone_number(number):
    if isinstance(number, basestring):
        match = PHONE_REGEX.search(number)
        if not match:
            raise ValueError("Invalid phone number")
        return match.groups()
    elif isinstance(number, (tuple, list)):
        if len(number) != 3:
            raise ValueError("Invalid phone number")
        return number
    else:
        raise ValueError("Invalid phone number")


def generate_cert_types(products):
    validations = {'domain': 'DV', 'extended': 'EV', 'organization': 'OV'}
    name_translation = maketrans(' -', '__')

    properties = []

    for product in products:
        name = (product.brandName + " " + product.name).upper().translate(name_translation, '()')

        args = map(repr, [product.id, product.brandName, product.name, validations[product.validationMethod]])
        if product.isWildcardSupported:
            args.append('is_wildcard=True')
        if product.isSgcSupported:
            args.append('is_sgc=True')
        if product.numberOfDomains > 1:
            args.append('is_multi=True')

        properties.append('    %s = CertType(%s)' % (name, ', '.join(args)))

    print("class CertTypes(BaseCertTypes):")
    print("    # Generated by openprovider.util.generate_cert_types")
    print()
    print("\n".join(sorted(properties)))
