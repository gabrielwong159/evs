import json

from flask import Blueprint, request
from operator import itemgetter

from clients.evs import EvsClient
from services.transaction import TransactionService
from routes import catch_errors

bp = Blueprint('transaction', __name__)


@bp.route('/transaction', methods=['POST'])
@catch_errors
def transaction():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    client = EvsClient()
    service = TransactionService(client)
    return json.dumps(service.get_transactions(username, password))


@bp.route('/transaction/demo', methods=['POST'])
@catch_errors
def transaction_demo():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    client = EvsClient()
    service = TransactionService(client)
    return json.dumps(service.get_transactions_demo(username, password))
