import json

from flask.wrappers import Response

from tests.base_test import BaseTest


class TestTransaction(BaseTest):
    def test_transaction_with_valid_credentials(self):
        response = self.transaction(self.username, self.password)
        self.assertEqual(response.status_code, 200)

    def test_transaction_with_invalid_credentials(self):
        username = 'foo'
        response = self.transaction(username, 'bar')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_data(as_text=True), f'Error on account login: {username}')

    def test_transaction_result_data_type(self):
        response = self.transaction(self.username, self.password)
        transactions = json.loads(response.data)
        self.assertEqual(type(transactions), list)
        for d in transactions:
            self.assertEqual(type(d['date']), str)
            self.assertEqual(type(d['amount']), float)

    def test_transaction_demo_with_valid_credentials(self):
        response = self.transaction_demo(self.username, self.password)
        self.assertEqual(response.status_code, 200)

    def test_transaction_demo_with_invalid_credentials(self):
        username = 'foo'
        response = self.transaction_demo(username, 'bar')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_data(as_text=True), f'Error on account login: {username}')

    def test_transaction_demo_result_data_type(self):
        response = self.transaction_demo(self.username, self.password)
        transactions = json.loads(response.data)
        self.assertEqual(type(transactions), list)
        for d in transactions:
            self.assertEqual(type(d['date']), str)
            self.assertEqual(type(d['amount']), float)

    def transaction(self, username: str, password: str) -> Response:
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'username': username, 'password': password})
        return self.client.post('/transaction', data=data, headers=headers)

    def transaction_demo(self, username: str, password: str) -> Response:
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'username': username, 'password': password})
        return self.client.post('/transaction/demo', data=data, headers=headers)
