import json

from flask import Blueprint, request
from operator import itemgetter

from clients.db import DbClient
from services.subscription import SubscriptionService

bp = Blueprint('subscription', __name__)


@bp.route('/subscription/<chat_id>')
def get_subscriptions_by_chat_id(chat_id):
    service = SubscriptionService(DbClient())
    return json.dumps(service.get_subscriptions_by_chat_id(chat_id))


@bp.route('/subscription', methods=['POST'])
def insert_subscription():
    body = request.get_json()
    username, amount, chat_id = itemgetter('username', 'amount', 'chat_id')(body)
    service = SubscriptionService(DbClient())
    service.insert_subscription(username, amount, chat_id)
    return 'Success'


@bp.route('/subscription/<subscription_id>', methods=['DELETE'])
def delete_subscription_by_id(subscription_id):
    service = SubscriptionService(DbClient())
    service.delete_subscription_by_id(subscription_id)
    return 'Success'
