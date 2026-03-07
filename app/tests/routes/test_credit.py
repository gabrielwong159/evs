import json

from flask.wrappers import Response

from tests.base_test import BaseTest


class TestCredit(BaseTest):
    def test_credit_can_be_converted_to_float(self):
        response = self.credit(self.username, self.password)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(float(response.data)), float)

    def test_credit_with_invalid_credentials(self):
        username = 'foo'
        response = self.credit(username, 'bar')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_data(as_text=True), f'Error on account login: {username}')

    def credit(self, username: str, password: str) -> Response:
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'username': username, 'password': password})
        return self.client.post('/credit', data=data, headers=headers)
