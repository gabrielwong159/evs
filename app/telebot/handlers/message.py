import re

from telegram.ext import Filters, MessageHandler

from app.settings import TELEGRAM_ADMIN_ID
from app.telebot.handlers.logging import logger


def admin_message_handler(update, context):
    if update.message.chat_id != int(TELEGRAM_ADMIN_ID):
        return
    if update.message.reply_to_message is None:
        return

    text = update.message.reply_to_message.text
    m = re.match(r'Message from (\d+):', text)
    if m is None:
        return

    target_user = int(m.group(1))
    logger.info(f'Admin reply to {target_user}')
    context.bot.send_message(chat_id=target_user, text=f'Message from admin:\n{update.message.text}')


message_handler = MessageHandler(Filters.text & ~Filters.command, admin_message_handler)
