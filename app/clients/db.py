from datetime import datetime

import psycopg2

from models.account import Account
from models.balance import UserBalance
from models.notification import Notification
from models.subscription import Subscription
from settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS


class DbClient:
    def _get_connection(self):
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
        )

    def _execute_and_commit(self, query: str) -> None:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()

    def _execute_and_fetchall(self, query: str) -> list:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    @staticmethod
    def _format_date(date) -> str:
        return '{:04d}/{:02d}/{:02d}'.format(date.year, date.month, date.day)

    # account

    def get_accounts(self) -> list[Account]:
        results = self._execute_and_fetchall("""
            SELECT username, password
            FROM account
        """)
        return [Account(*row) for row in results]

    def insert_account(self, username: str, password: str) -> None:
        self._execute_and_commit(f"""
            INSERT INTO account (username, password)
            VALUES ('{username}', '{password}')
            ON CONFLICT DO NOTHING
        """)

    # balance

    def get_balances_by_username(self, username: str) -> list[tuple[str, float]]:
        rows = self._execute_and_fetchall(f"""
            SELECT retrieve_date, amount
            FROM balance
            WHERE username = '{username}'
            ORDER BY id
        """)
        return [(self._format_date(date), amount) for date, amount in rows]

    def get_balances_by_username_before(self, username: str, cutoff: datetime) -> list[tuple[str, float]]:
        rows = self._execute_and_fetchall(f"""
            SELECT retrieve_date, amount
            FROM balance
            WHERE username = '{username}'
                AND retrieve_date <= '{self._format_date(cutoff)}'
            ORDER BY id
        """)
        return [(self._format_date(date), amount) for date, amount in rows]

    def get_latest_balances_by_chat_id(self, chat_id: int) -> list[UserBalance]:
        rows = self._execute_and_fetchall(f"""
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
        """)
        return [UserBalance(*row) for row in rows]

    def insert_balance(self, username: str, retrieve_date: str, amount: float) -> None:
        self._execute_and_commit(f"""
            INSERT INTO balance (username, retrieve_date, amount)
            VALUES ('{username}', '{retrieve_date}', {amount})
        """)

    # subscription

    def get_subscriptions_by_chat_id(self, chat_id: int) -> list[Subscription]:
        rows = self._execute_and_fetchall(f"""
            SELECT id, username, amount, chat_id
            FROM subscription
            WHERE chat_id = {chat_id}
        """)
        return [Subscription(*row) for row in rows]

    def insert_subscription(self, username: str, amount: float, chat_id: int) -> None:
        self._execute_and_commit(f"""
            INSERT INTO subscription (username, amount, chat_id)
            VALUES ('{username}', '{amount}', '{chat_id}')
            ON CONFLICT DO NOTHING
        """)

    def delete_subscription_by_id(self, id: int) -> None:
        self._execute_and_commit(f"""
            DELETE FROM subscription
            WHERE id = {id}
        """)

    # notification

    def get_notifications(self) -> list[Notification]:
        rows = self._execute_and_fetchall("""
            CREATE TEMP VIEW all_notes AS (
                SELECT DISTINCT balance.username, balance.amount, chat_id
                FROM subscription
                INNER JOIN (
                   SELECT id, username, amount
                   FROM balance
                   WHERE balance.id IN (
                       SELECT MAX(id) FROM balance GROUP BY username
                   )
                ) AS balance
                ON balance.username = subscription.username
                   AND balance.amount <= subscription.amount
            );

            CREATE TEMP VIEW latest_notes AS (
                SELECT username, chat_id, message_date
                FROM notification
                WHERE notification.id IN (
                    SELECT MAX (id) FROM notification GROUP BY username, chat_id
                )
            );

            SELECT username, amount, chat_id
            FROM all_notes
            LEFT JOIN latest_notes
            USING (username, chat_id)
            WHERE latest_notes.message_date <= CURRENT_DATE - interval '3 days'
                OR (latest_notes.username IS NULL AND latest_notes.chat_id IS NULL);
        """)
        return [Notification(*row) for row in rows]

    def insert_notification(self, username: str, chat_id: int, message_date: str) -> None:
        self._execute_and_commit(f"""
            INSERT INTO notification (username, chat_id, message_date)
            VALUES ('{username}', {chat_id}, '{message_date}')
        """)

    # command

    def insert_command(self, name: str, chat_id: int, is_completed: bool, is_cancelled: bool) -> None:
        self._execute_and_commit(f"""
            INSERT INTO command (name, chat_id, is_completed, is_cancelled)
            VALUES ('{name}', {chat_id}, {'TRUE' if is_completed else 'FALSE'}, {'TRUE' if is_cancelled else 'FALSE'})
        """)
