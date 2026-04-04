from telegram.ext import Updater

from app.settings import TELEGRAM_TOKEN
from app.telebot.handlers import commands as cmd, message
from app.telebot.handlers.conv import (add_subscription as add,
                                       view_subscription as view,
                                       feedback)


class Bot:
    def __init__(self):
        self.updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def add_handlers(self):
        for handler in cmd.handlers:
            self.dispatcher.add_handler(handler)
        self.dispatcher.add_handler(add.conv_handler)
        self.dispatcher.add_handler(view.conv_handler)
        self.dispatcher.add_handler(feedback.conv_handler)
        self.dispatcher.add_handler(message.message_handler)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()
