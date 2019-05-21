import sys
sys.path.insert(0, '..')

import psycopg2
from collections import namedtuple


def get_accounts() -> list:
    query = """SELECT * FROM account;"""
    rows = execute_and_fetchall(query)
    Account = namedtuple('Account', 'username password')
    return [Account(*row) for row in rows]


def insert_account(username: str, password: str):
    query = f"""INSERT INTO account (username, password)
                VALUES ('{username}', '{password}')
                ON CONFLICT DO NOTHING;"""
    execute_and_commit(query)


def get_balances_by_username(username) -> list:
    if not username_valid(username):
        return []

    def parse_date(date):
        return '{:04d}/{:02d}/{:02d}'.format(date.year, date.month, date.day)

    query = f"""SELECT retrieve_date, amount
                FROM balance
                WHERE username = '{username}'
                ORDER BY id;"""
    rows = execute_and_fetchall(query)
    return [(parse_date(date), amount) for date, amount in rows]


def insert_balance(username, retrieve_date, amount):
    query = f"""INSERT INTO balance (username, retrieve_date, amount) 
                VALUES ('{username}', '{retrieve_date}', {amount});"""
    execute_and_commit(query)


def get_subscriptions_by_chat_id(chat_id: int) -> list:
    query = f"""SELECT * FROM subscription
                WHERE chat_id = {chat_id};"""
    rows = execute_and_fetchall(query)
    Subscription = namedtuple('Subscription', 'id username amount chat_id')
    return [Subscription(*row) for row in rows]


def insert_subscription(username: str, amount: str, chat_id: int) -> bool:
    if not username_valid(username):
        return False

    query = f"""INSERT INTO subscription (username, amount, chat_id)
                VALUES ('{username}', '{amount}', '{chat_id}')
                ON CONFLICT DO NOTHING;"""
    execute_and_commit(query)
    return True


def delete_subscription_by_id(id: int) -> bool:
    # validate id
    all_subscription_ids = set(subscription.id for subscription in get_subscriptions())
    if id not in all_subscription_ids:
        return False

    query = f"""DELETE FROM subscription
                WHERE id = {id};"""
    execute_and_commit(query)
    return True


def get_notifications() -> list:
    query = """SELECT balance.username, balance.amount, chat_id
               FROM subscription
               INNER JOIN (
                   SELECT *
                   FROM balance
                   WHERE balance.id IN (
                       SELECT MAX (id) FROM balance GROUP BY username
                   )
               ) AS balance
               ON balance.username = subscription.username
               AND balance.amount <= subscription.amount;"""
    rows = execute_and_fetchall(query)
    Notification = namedtuple('Notification', 'username amount chat_id')
    return [Notification(*row) for row in rows]


def username_valid(username: str) -> bool:
    """
    Ensures that input username is valid (i.e. exists in database).

    :param username: username of length 8 (by SUTD EVS standard)
    :return: True if valid
    """
    all_usernames = set(acc.username for acc in get_accounts())
    return username in all_usernames


def execute_and_commit(query):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()


def execute_and_fetchall(query) -> list:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
    return rows


def get_connection():
    dbname = 'evs'
    user = 'ubuntu'
    conn = psycopg2.connect(dbname=dbname, user=user)
    return conn
