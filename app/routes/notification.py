import json

from flask import Blueprint, request
from operator import itemgetter

from clients.db import DbClient
from services.notification import NotificationService

bp = Blueprint('notification', __name__)


@bp.route('/notification', methods=['GET'])
def get_notifications():
    service = NotificationService(DbClient())
    return json.dumps(service.get_notifications())


@bp.route('/notification', methods=['POST'])
def insert_notification():
    body = request.get_json()
    username, chat_id, message_date = itemgetter('username', 'chat_id', 'message_date')(body)
    service = NotificationService(DbClient())
    service.insert_notification(username, chat_id, message_date)
    return 'Success'
