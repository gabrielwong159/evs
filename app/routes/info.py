import json
import logging
import os

from flask import Blueprint, request
from operator import itemgetter

from app.clients.db import DbClient
from app.clients.evs import EvsClient
from app.models.exception import LoginError
from app.services.account import AccountService
from app.services.db_balance import DbBalanceService
from app.services.transaction import TransactionService

bp = Blueprint('info', __name__)

logger = logging.getLogger(__name__)

DEMO_JSON_PATH = os.environ.get('DEMO_JSON_PATH', 'demo.json')


@bp.route('/info', methods=['POST'])
def get_info():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    logger.info(f'({username}, {password})')

    accounts = AccountService(DbClient()).get_accounts()
    if not any(a.username == username and a.password == password for a in accounts):
        return 'Account not found', 404

    return json.dumps(_build_info(username, password))


@bp.route('/info/demo')
def get_demo_info():
    logger.info('Demo')

    with open(DEMO_JSON_PATH) as f:
        obj = json.load(f)
    username, password = itemgetter('username', 'password')(obj)

    return json.dumps(_build_info(username, password, demo=True))


def _build_info(username: str, password: str, demo=False) -> dict:
    db_client = DbClient()
    balance_service = DbBalanceService(db_client)
    balances = balance_service.get_demo_balances_by_username(username) if demo \
        else balance_service.get_balances_by_username(username)

    try:
        txn_service = TransactionService(EvsClient())
        transactions = txn_service.get_transactions_demo(username, password) if demo \
            else txn_service.get_transactions(username, password)
    except LoginError:
        transactions = []

    return {'balances': balances, 'transactions': transactions}
