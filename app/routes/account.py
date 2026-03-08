import json

from flask import Blueprint, request
from operator import itemgetter

from clients.db import DbClient
from services.account import AccountService

bp = Blueprint('account', __name__)


@bp.route('/account', methods=['GET', 'POST'])
def account():
    service = AccountService(DbClient())
    if request.method == 'GET':
        accounts = service.get_accounts()
        return json.dumps(accounts)
    elif request.method == 'POST':
        body = request.get_json()
        username, password = itemgetter('username', 'password')(body)
        service.insert_account(username, password)
        return 'Success'
