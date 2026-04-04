import logging

from app.clients.db import DbClient
from app.services.command import CommandService

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def log_command_in_db(name: str, chat_id: int,
                      is_completed: bool, is_cancelled: bool) -> None:
    CommandService(DbClient()).insert_command(name, chat_id, is_completed, is_cancelled)
