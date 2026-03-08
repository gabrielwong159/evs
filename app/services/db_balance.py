from datetime import datetime

from clients.db import DbClient
from models.balance import UserBalance
from services.account import AccountService

DEMO_CUTOFF_DATE = datetime(2019, 8, 24)


class DbBalanceService:
    def __init__(self, client: DbClient):
        self._db = client
        self._accounts = AccountService(client)

    def get_balances_by_username(self, username: str) -> list:
        if not self._accounts.username_valid(username):
            return []
        return self._db.get_balances_by_username(username)

    def get_demo_balances_by_username(self, username: str, cutoff=DEMO_CUTOFF_DATE) -> list:
        if not self._accounts.username_valid(username):
            return []
        return self._db.get_balances_by_username_before(username, cutoff)

    def get_latest_balances_by_chat_id(self, chat_id: int) -> list[UserBalance]:
        return sorted(self._db.get_latest_balances_by_chat_id(chat_id))

    def insert_balance(self, username: str, retrieve_date: str, amount: float) -> None:
        self._db.insert_balance(username, retrieve_date, amount)
