from functools import wraps

from flask import request
from requests.exceptions import ConnectionError

from models.exception import LoginError


def catch_errors(route_func):
    @wraps(route_func)
    def inner(*args, **kwargs):
        try:
            return route_func(*args, **kwargs)
        except ConnectionError:
            return 'Could not access EVS web', 503
        except LoginError:
            username = request.get_json()['username']
            return f'Error on account login: {username}', 404
    return inner
