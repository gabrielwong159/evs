from datetime import datetime

from clients.evs import EvsClient
from models.exception import LoginError


class TransactionService:
    def __init__(self, client: EvsClient):
        self._evs_client = client

    def get_transactions(self, username: str, password: str) -> list:
        if not self._evs_client.login(username, password):
            raise LoginError('Wrong login credentials')
        return self._evs_client.get_transactions()

    def get_transactions_demo(self, username: str, password: str, cutoff=datetime(2019, 8, 24)) -> list:
        transactions = self.get_transactions(username, password)
        return [txn for txn in transactions
                if datetime.strptime(txn['date'], '%Y-%m-%d') <= cutoff]
