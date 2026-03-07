from datetime import datetime

from bs4 import BeautifulSoup

from clients.evs import EvsClient
from models.transaction import Transaction
from services.transaction import TransactionService
from tests.base_test import BaseTest


class TestTransactionService(BaseTest):
    def test_row_to_transaction(self):
        data = ('<tr>'
                '  <td>transaction_id</td>'
                '  <td>date</td>'
                '  <td>amount</td>'
                '  <td>offer_id</td>'
                '  <td>payment_mode</td>'
                '  <td>channel</td>'
                '  <td>status</td>'
                '</tr>')
        soup = BeautifulSoup(data, 'html.parser')
        result = EvsClient._row_to_transaction(soup.tr)

        txn = Transaction(transaction_id='transaction_id',
                          date='date',
                          amount='amount',
                          offer_id='offer_id',
                          payment_mode='payment_mode',
                          channel='channel',
                          status='status')
        self.assertEqual(result, txn)

    def test_transaction_to_dict(self):
        data = Transaction(date='01/01/2019 00:00', amount='10.00',
                           transaction_id=None, offer_id=None, payment_mode=None, channel=None, status=None)
        result = EvsClient._transaction_to_dict(data)
        self.assertEqual(result, {'date': '2019-01-01', 'amount': 10})

    def test_get_transactions(self):
        service = TransactionService(EvsClient())
        transactions = service.get_transactions(self.username, self.password)
        self.assertEqual(type(transactions), list)

    def test_get_transactions_attributes(self):
        service = TransactionService(EvsClient())
        transactions = service.get_transactions(self.username, self.password)
        for txn in transactions:
            self.assertEqual(type(txn), dict)
            self.assertEqual(type(txn['date']), str)
            self.assertEqual(type(txn['amount']), float)

    def test_get_transactions_demo(self):
        service = TransactionService(EvsClient())
        transactions = service.get_transactions_demo(self.username, self.password)
        self.assertEqual(type(transactions), list)

    def test_get_transactions_demo_attributes(self):
        service = TransactionService(EvsClient())
        transactions = service.get_transactions_demo(self.username, self.password)
        for txn in transactions:
            self.assertEqual(type(txn), dict)
            self.assertEqual(type(txn['date']), str)
            self.assertEqual(type(txn['amount']), float)

    def test_get_transactions_demo_cutoff(self):
        cutoff = datetime(2019, 6, 1)
        service = TransactionService(EvsClient())
        transactions = service.get_transactions_demo(self.username, self.password, cutoff)
        for txn in transactions:
            self.assertLessEqual(datetime.strptime(txn['date'], '%Y-%m-%d'), cutoff)
