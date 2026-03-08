from clients.db import DbClient
from models.account import Account


class AccountService:
    def __init__(self, client: DbClient):
        self._db = client

    def get_accounts(self) -> list[Account]:
        return self._db.get_accounts()

    def insert_account(self, username: str, password: str) -> None:
        self._db.insert_account(username, password)

    def username_valid(self, username: str) -> bool:
        all_usernames = {acc.username for acc in self._db.get_accounts()}
        return username in all_usernames
