# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from time import sleep
from unittest import skipUnless

import pytest
from django.test import SimpleTestCase, TestCase
from django.utils import six

from django_mysql.utils import (
    PTFingerprintThread, WeightedAverageRate, have_program, index_name,
    pt_fingerprint
)
from testapp.models import Author, AuthorMultiIndex


class WeightedAverageRateTests(SimpleTestCase):

    def test_constant(self):
        # If we keep achieving a rate of 100 rows in 0.5 seconds, it should
        # recommend that we keep there
        rate = WeightedAverageRate(0.5)
        assert rate.update(100, 0.5) == 100
        assert rate.update(100, 0.5) == 100
        assert rate.update(100, 0.5) == 100

    def test_slow(self):
        # If we keep achieving a rate of 100 rows in 1 seconds, it should
        # recommend that we move to 50
        rate = WeightedAverageRate(0.5)
        assert rate.update(100, 1.0) == 50
        assert rate.update(100, 1.0) == 50
        assert rate.update(100, 1.0) == 50

    def test_fast(self):
        # If we keep achieving a rate of 100 rows in 0.25 seconds, it should
        # recommend that we move to 200
        rate = WeightedAverageRate(0.5)
        assert rate.update(100, 0.25) == 200
        assert rate.update(100, 0.25) == 200
        assert rate.update(100, 0.25) == 200

    def test_good_guess(self):
        # If we are first slow then hit the target at 50, we should be good
        rate = WeightedAverageRate(0.5)
        assert rate.update(100, 1.0) == 50
        assert rate.update(50, 0.5) == 50
        assert rate.update(50, 0.5) == 50
        assert rate.update(50, 0.5) == 50

    def test_zero_division(self):
        rate = WeightedAverageRate(0.5)
        assert rate.update(1, 0.0) == 500


@skipUnless(have_program('pt-fingerprint'),
            "pt-fingerprint must be installed")
class PTFingerprintTests(SimpleTestCase):

    def test_basic(self):
        assert pt_fingerprint('SELECT 5') == 'select ?'
        assert pt_fingerprint('SELECT 5;') == 'select ?'

    def test_long(self):
        query = """
            SELECT
                CONCAT(customer.last_name, ', ', customer.first_name)
                    AS customer,
                address.phone,
                film.title
            FROM rental
                INNER JOIN customer
                    ON rental.customer_id = customer.customer_id
                INNER JOIN address
                    ON customer.address_id = address.address_id
                INNER JOIN inventory
                    ON rental.inventory_id = inventory.inventory_id
                INNER JOIN film
                    ON inventory.film_id = film.film_id
            WHERE
                rental.return_date IS NULL AND
                rental_date + INTERVAL film.rental_duration DAY <
                    CURRENT_DATE()
            LIMIT 5"""
        assert (
            pt_fingerprint(query) ==
            "select concat(customer.last_name, ?, customer.first_name) as "
            "customer, address.phone, film.title from rental inner join "
            "customer on rental.customer_id = customer.customer_id inner join "
            "address on customer.address_id = address.address_id inner join "
            "inventory on rental.inventory_id = inventory.inventory_id inner "
            "join film on inventory.film_id = film.film_id where "
            "rental.return_date is ? and rental_date ? interval "
            "film.rental_duration day < current_date() limit ?"
        )

    def test_the_thread_shuts_on_time_out(self):
        PTFingerprintThread.PROCESS_LIFETIME = 0.1
        pt_fingerprint("select 123")
        sleep(0.2)
        assert PTFingerprintThread.the_thread is None
        PTFingerprintThread.PROCESS_LIFETIME = 60


class IndexNameTests(TestCase):
    def test_requires_field_names(self):
        with pytest.raises(ValueError) as excinfo:
            index_name(Author)
        assert (
            "At least one field name required" in
            six.text_type(excinfo.value)
        )

    def test_requires_real_field_names(self):
        with pytest.raises(ValueError) as excinfo:
            index_name(Author, 'nonexistent')
        assert (
            "Fields do not exist: nonexistent" in
            six.text_type(excinfo.value)
        )

    def test_invalid_kwarg(self):
        with pytest.raises(ValueError) as excinfo:
            index_name(Author, 'name', nonexistent_kwarg=True)
        assert (
            "The only supported keyword argument is 'using'" in
            six.text_type(excinfo.value)
        )

    def test_primary_key(self):
        assert index_name(Author, 'id') == 'PRIMARY'

    def test_primary_key_using_other(self):
        assert index_name(Author, 'id', using='other') == 'PRIMARY'

    def test_secondary_single_field(self):
        name = index_name(Author, 'name')
        assert name.startswith('testapp_author_')

    def test_index_does_not_exist(self):
        with pytest.raises(KeyError) as excinfo:
            index_name(Author, 'bio')
        assert "There is no index on (bio)" in six.text_type(excinfo.value)

    def test_secondary_multiple_fields(self):
        name = index_name(AuthorMultiIndex, 'name', 'country')
        assert name.startswith('testapp_authormultiindex')

    def test_secondary_multiple_fields_non_existent_reversed_existent(self):
        # Checks that order is preserved
        with pytest.raises(KeyError):
            index_name(AuthorMultiIndex, 'country', 'name')

    def test_secondary_multiple_fields_non_existent(self):
        with pytest.raises(KeyError):
            index_name(AuthorMultiIndex, 'country', 'id')
