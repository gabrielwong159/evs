from clients.db import DbClient
from models.notification import Notification


class NotificationService:
    def __init__(self, client: DbClient):
        self._db = client

    def get_notifications(self) -> list[Notification]:
        return self._db.get_notifications()

    def insert_notification(self, username: str, chat_id: int, message_date: str) -> None:
        self._db.insert_notification(username, chat_id, message_date)
