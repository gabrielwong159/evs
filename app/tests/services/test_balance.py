from clients.evs import EvsClient
from models.exception import LoginError
from services.balance import BalanceService
from tests.base_test import BaseTest


class TestGetAmount(BaseTest):
    def test_successful_login(self):
        service = BalanceService(EvsClient())
        amount = service.get_amount(self.username, self.password)
        self.assertEqual(type(amount), float)

    def test_unsuccessful_login(self):
        service = BalanceService(EvsClient())
        with self.assertRaises(LoginError):
            service.get_amount('foo', 'bar')
