from clients.db import DbClient
from models.subscription import Subscription
from services.account import AccountService


class SubscriptionService:
    def __init__(self, client: DbClient):
        self._db = client
        self._accounts = AccountService(client)

    def get_subscriptions_by_chat_id(self, chat_id: int) -> list[Subscription]:
        return self._db.get_subscriptions_by_chat_id(chat_id)

    def insert_subscription(self, username: str, amount: float, chat_id: int) -> None:
        if not self._accounts.username_valid(username):
            return
        self._db.insert_subscription(username, amount, chat_id)

    def delete_subscription_by_id(self, id: int) -> None:
        self._db.delete_subscription_by_id(id)
