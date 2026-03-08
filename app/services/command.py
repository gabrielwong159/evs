from clients.db import DbClient


class CommandService:
    def __init__(self, client: DbClient):
        self._db = client

    def insert_command(self, name: str, chat_id: int, is_completed: bool, is_cancelled: bool) -> None:
        self._db.insert_command(name, chat_id, is_completed, is_cancelled)
