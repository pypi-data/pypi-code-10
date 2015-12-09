import unittest

from quickbooks.objects.vendor import Vendor, ContactInfo


class VendorTests(unittest.TestCase):
    def test_unicode(self):
        vendor = Vendor()
        vendor.DisplayName = "test"

        self.assertEqual(str(vendor), "test")

    def test_to_ref(self):
        vendor = Vendor()
        vendor.DisplayName = "test"
        vendor.Id = 100

        ref = vendor.to_ref()

        self.assertEqual(ref.name, "test")
        self.assertEqual(ref.type, "Vendor")
        self.assertEqual(ref.value, 100)


class ContactInfoTests(unittest.TestCase):
    def test_init(self):
        contact_info = ContactInfo()

        self.assertEqual(contact_info.Type, "")
        self.assertEqual(contact_info.Telephone, None)
