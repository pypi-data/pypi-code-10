import unittest

from quickbooks.objects.employee import Employee


class EmployeeTests(unittest.TestCase):
    def test_unicode(self):
        employee = Employee()
        employee.DisplayName = "test"

        self.assertEqual(str(employee), "test")

    def test_to_ref(self):
        employee = Employee()
        employee.DisplayName = "test"
        employee.Id = 100

        ref = employee.to_ref()

        self.assertEqual(ref.name, "test")
        self.assertEqual(ref.type, "Employee")
        self.assertEqual(ref.value, 100)
