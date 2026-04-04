from datetime import datetime
from operator import attrgetter

from app.clients.db import DbClient
from app.clients.telemsg import TelegramClient
from app.services.notification import NotificationService


def get_date():
    now = datetime.now()
    return '{:04d}/{:02d}/{:02d}'.format(now.year, now.month, now.day)


def make_text(notification):
    username, amount = attrgetter('username', 'amount')(notification)
    return (f'Aircon notification for account {username}: '
            f'your remaining balance is ${amount:.2f}.\n\n'
            f'You will be notified a maximum of once every 3 days.')


def main():
    db_client = DbClient()
    notification_service = NotificationService(db_client)
    telegram_client = TelegramClient()
    date = get_date()

    for n in notification_service.get_notifications():
        telegram_client.send_message(n.chat_id, make_text(n))
        notification_service.insert_notification(n.username, n.chat_id, date)


if __name__ == '__main__':
    main()
