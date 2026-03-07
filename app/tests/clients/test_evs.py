from unittest import TestCase

from clients.evs import EvsClient
from tests.base_test import BaseTest


class TestGetBalanceFromText(TestCase):
    def test_return_type(self):
        text = 'S$ 0.00' * 2
        result = EvsClient._get_balance_from_text(text)
        self.assertEqual(type(result), float)

    def test_zero(self):
        text = 'S$ 0.00' * 2
        self.assertEqual(EvsClient._get_balance_from_text(text), 0)

    def test_less_than_ten(self):
        text = 'S$ 9.99' * 2
        self.assertEqual(EvsClient._get_balance_from_text(text), 9.99)

    def test_less_than_hundred(self):
        text = 'S$ 99.99' * 2
        self.assertEqual(EvsClient._get_balance_from_text(text), 99.99)

    def test_less_than_thousand(self):
        text = 'S$ 999.999' * 2
        self.assertEqual(EvsClient._get_balance_from_text(text), 999.99)

    def test_less_than_million(self):
        text = 'S$ 999,999.99' * 2
        self.assertEqual(EvsClient._get_balance_from_text(text), 999_999.99)

    def test_less_than_billion(self):
        text = 'S$ 999,999,999.99' * 2
        self.assertEqual(EvsClient._get_balance_from_text(text), 999_999_999.99)

    def test_empty_string(self):
        with self.assertRaises(AssertionError):
            EvsClient._get_balance_from_text('')

    def test_one_match(self):
        with self.assertRaises(AssertionError):
            EvsClient._get_balance_from_text('S$ 0.00')

    def test_no_decimal(self):
        with self.assertRaises(AssertionError):
            EvsClient._get_balance_from_text('S$ 10' * 2)


class TestEvsClientLogin(BaseTest):
    def test_login_is_valid(self):
        client = EvsClient()
        result = client.login(self.username, self.password)
        self.assertTrue(result)

    def test_login_is_invalid(self):
        client = EvsClient()
        result = client.login('foo', 'bar')
        self.assertFalse(result)
