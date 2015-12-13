from unittest import TestCase
from bucket_filter import *

class RegisterTest(TestCase):

    def basic_test(self):
        register_bucket("adult=true")
        self.assertIsNotNone(get_bucket("adult=true"))

    def test_with_elements(self):
        register_bucket("opensource=true", [{"id" : 1, "value" : "field"}, {"id" : 2, "name" : "value"}])
        bucket = get_bucket("opensource=true")
        self.assertEqual("opensource=true", bucket.condition.expression, "Condition in bucket has incorrect expression")
        self.assertEqual(2, len(bucket.elements), "Did not propogate elements into bucket")

class SolveTest(TestCase):

    def basic_and_test(self):
        register_bucket("opensource=true", [{"id" : 1, "value" : "field"}, {"id" : 2, "name" : "value"}])
        register_bucket("activeDev=false", [{"id" : 1, "value" : "field"}, {"id" : 4, "name" : "value"}])
        answer = solve("opensource=true & activeDev=false")
        self.assertEqual(1, len(answer))
        self.assertEqual(1, answer[0]["id"])

    def basic_or_test(self):
        register_bucket("opensource=true", [{"id" : 1, "value" : "field"}, {"id" : 2, "name" : "value"}])
        register_bucket("activeDev=false", [{"id" : 1, "value" : "field"}, {"id" : 4, "name" : "value"}])
        answer = solve("opensource=true || activeDev=false")
        self.assertEqual(3, len(answer))
