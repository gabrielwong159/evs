from flask import Blueprint, request
from operator import itemgetter

from clients.evs import EvsClient
from services.balance import BalanceService
from routes import catch_errors

bp = Blueprint('credit', __name__)


@bp.route('/credit', methods=['POST'])
@catch_errors
def credit():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    client = EvsClient()
    service = BalanceService(client)
    return str(service.get_amount(username, password))
