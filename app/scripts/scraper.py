from datetime import datetime

from app.clients.db import DbClient
from app.clients.evs import EvsClient
from app.models.exception import LoginError
from app.services.account import AccountService
from app.services.balance import BalanceService
from app.services.db_balance import DbBalanceService


def get_date():
    now = datetime.now()
    return '{:04d}/{:02d}/{:02d}'.format(now.year, now.month, now.day)


def main():
    db_client = DbClient()
    accounts = AccountService(db_client).get_accounts()
    balance_service = BalanceService(EvsClient())
    db_balance_service = DbBalanceService(db_client)
    date = get_date()

    for account in accounts:
        print(account)
        try:
            amount = balance_service.get_amount(account.username, account.password)
        except LoginError as e:
            print('Warning: error retrieving account:', e)
            continue
        db_balance_service.insert_balance(account.username, date, amount)


if __name__ == '__main__':
    main()
