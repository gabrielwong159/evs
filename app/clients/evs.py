import re
import requests
import bs4
from bs4 import BeautifulSoup
from datetime import datetime

from models.transaction import Transaction

BASE_URL = 'https://nus-utown.evs.com.sg/SUTDMain'
LOGIN_URL = f'{BASE_URL}/loginServlet'
CREDIT_URL = f'{BASE_URL}/viewMeterCreditServlet'
TRANSACTION_URL = f'{BASE_URL}/listTransactionServlet'


class EvsClient:
    def __init__(self):
        self._session = requests.Session()

    def login(self, username: str, password: str) -> bool:
        data = {
            'txtLoginId': username,
            'txtPassword': password,
            'btnLogin': 'Login',
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = self._session.post(url=LOGIN_URL, data=data, headers=headers, verify=False)
        return 'Invalid' not in r.url

    def get_credit(self) -> float:
        r = self._session.get(CREDIT_URL)
        return self._get_balance_from_text(r.text)

    def get_transactions(self) -> list:
        r = self._session.get(TRANSACTION_URL)
        return self._parse_html(r.text)

    @staticmethod
    def _get_balance_from_text(text: str) -> float:
        pattern = r'S\$ ((\d{1,3},)*\d{1,3}\.\d{2})'
        matches = re.findall(pattern, text)
        assert len(matches) > 1, 'Could not find balance on page'
        match = matches[0][0].replace(',', '')
        return float(match)

    @staticmethod
    def _parse_html(html_text: str) -> list:
        soup = BeautifulSoup(html_text, 'html.parser')
        rows = soup.find_all('tr', attrs='tblRow')
        transactions = (EvsClient._row_to_transaction(row) for row in rows)
        return [EvsClient._transaction_to_dict(txn) for txn in transactions]

    @staticmethod
    def _row_to_transaction(row: bs4.element.Tag) -> Transaction:
        args = (elem.text.strip() for elem in row.find_all('td'))
        return Transaction(*args)

    @staticmethod
    def _transaction_to_dict(txn: Transaction) -> dict:
        date_obj = datetime.strptime(txn.date, '%d/%m/%Y %H:%M')
        date_str = date_obj.strftime('%Y-%m-%d')
        amount = float(txn.amount)
        return {'date': date_str, 'amount': amount}
