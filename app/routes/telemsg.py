from flask import Blueprint, request

from clients.telemsg import TelegramClient
from settings import TELEGRAM_ADMIN_ID

bp = Blueprint('telemsg', __name__)


@bp.route('/message', methods=['POST'])
def message():
    body = request.get_json()
    chat_id = body['chat_id']
    text = body['text']
    success = TelegramClient().send_message(chat_id, text)
    return 'Success' if success else 'Fail'


@bp.route('/message/admin', methods=['POST'])
def message_admin():
    body = request.get_json()
    chat_id = body['chat_id']
    text = f"Message from {chat_id}:\n{body['text']}"
    success = TelegramClient().send_message(TELEGRAM_ADMIN_ID, text)
    return 'Success' if success else 'Fail'
