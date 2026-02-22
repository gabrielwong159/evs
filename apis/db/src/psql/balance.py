from collections import namedtuple
from datetime import datetime
from typing import List, NamedTuple
from .exec import execute_and_commit, execute_and_fetchall
from .account import username_valid

DEMO_CUTOFF_DATE = datetime(2019, 8, 24)
UserBalance = namedtuple('UserBalance', 'username, amount')


def get_balances_by_username(username: str) -> List[tuple]:
    if not username_valid(username):
        return []

    def parse_date(date):
        return '{:04d}/{:02d}/{:02d}'.format(date.year, date.month, date.day)

    query = f"""
        SELECT retrieve_date, amount
        FROM balance
        WHERE username = '{username}'
        ORDER BY id
    """
    rows = execute_and_fetchall(query)
    return [(parse_date(date), amount) for date, amount in rows]


def get_demo_balances_by_username(username: str, cutoff=DEMO_CUTOFF_DATE) -> list:
    if not username_valid(username):
        return []

    def parse_date(date):
        return '{:04d}/{:02d}/{:02d}'.format(date.year, date.month, date.day)

    query = f"""
        SELECT retrieve_date, amount
        FROM balance
        WHERE username = '{username}'
            AND retrieve_date <= '{parse_date(cutoff)}'
        ORDER BY id
    """
    rows = execute_and_fetchall(query)
    return [(parse_date(date), amount) for date, amount in rows]


def get_latest_balances_by_chat_id(chat_id: int) -> List[NamedTuple]:
    query = f"""
        SELECT DISTINCT balance.username, balance.amount
        FROM subscription
        INNER JOIN (
            SELECT id, username, amount
            FROM balance
            WHERE balance.id IN (
                SELECT MAX(id) FROM balance GROUP BY username
            )
        ) AS balance
        ON subscription.username = balance.username
            AND subscription.chat_id = {chat_id}
    """
    rows = execute_and_fetchall(query)
    return sorted(UserBalance(*row) for row in rows)


def insert_balance(username, retrieve_date, amount) -> None:
    query = f"""INSERT INTO balance (username, retrieve_date, amount) 
                VALUES ('{username}', '{retrieve_date}', {amount});"""
    execute_and_commit(query)
