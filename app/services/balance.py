from app.clients.evs import EvsClient
from app.models.exception import LoginError


class BalanceService:
    def __init__(self, client: EvsClient):
        self._evs_client = client

    def get_amount(self, username: str, password: str) -> float:
        if not self._evs_client.login(username, password):
            raise LoginError('Wrong login credentials')
        return self._evs_client.get_credit()
