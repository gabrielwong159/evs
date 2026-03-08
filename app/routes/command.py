from flask import Blueprint, request
from operator import itemgetter

from clients.db import DbClient
from services.command import CommandService

bp = Blueprint('command', __name__)


@bp.route('/command', methods=['POST'])
def insert_command():
    body = request.get_json()
    name, chat_id, is_completed, is_cancelled = itemgetter('name', 'chat_id', 'is_completed', 'is_cancelled')(body)
    service = CommandService(DbClient())
    service.insert_command(name, chat_id, is_completed, is_cancelled)
    return 'Success'
