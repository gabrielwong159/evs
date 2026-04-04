import json

from flask import Blueprint, request
from operator import itemgetter

from app.clients.db import DbClient
from app.services.db_balance import DbBalanceService

bp = Blueprint('balance', __name__)


@bp.route('/balance/chatid/<chat_id>')
def get_latest_balances_by_chat_id(chat_id):
    service = DbBalanceService(DbClient())
    return json.dumps(service.get_latest_balances_by_chat_id(chat_id))


@bp.route('/balance', methods=['POST'])
def insert_balance():
    body = request.get_json()
    username, retrieve_date, amount = itemgetter('username', 'retrieve_date', 'amount')(body)
    service = DbBalanceService(DbClient())
    service.insert_balance(username, retrieve_date, amount)
    return 'Success'
