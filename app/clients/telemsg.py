import requests

from settings import TELEGRAM_TOKEN

BASE_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'


class TelegramClient:
    def send_message(self, chat_id: int, text: str) -> bool:
        url = f'{BASE_URL}/sendMessage'
        r = requests.post(url, json={'chat_id': chat_id, 'text': text})
        return r.ok
