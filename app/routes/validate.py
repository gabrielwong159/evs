import json

from flask import Blueprint, request
from operator import itemgetter

from app.clients.evs import EvsClient
from app.routes import catch_errors

bp = Blueprint('validate', __name__)


@bp.route('/validate', methods=['POST'])
@catch_errors
def validate():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    return json.dumps({'valid': EvsClient().login(username, password)})
