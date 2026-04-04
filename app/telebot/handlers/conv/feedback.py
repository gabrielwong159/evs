from enum import Enum

from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from app.settings import TELEGRAM_ADMIN_ID
from app.telebot.handlers.logging import logger, log_command_in_db

COMMAND_NAME = 'feedback'


class States(Enum):
    FEEDBACK, CANCEL = range(2)


def start(update, context):
    update.message.reply_text(
        'Hi! Feel free to leave a message here. '
        'Feedback or bug reports are always welcome. '
        'Anything you type next will be forwarded to the admin.\n\n'
        'Note that this bot has no affiliation with the EVS vendor. '
        'Issues with login or balance not updating should be raised '
        'with the vendor directly. Thank you!\n\n'
        'Type /cancel to cancel.'
    )
    return States.FEEDBACK


def feedback(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f'({chat_id}) Feedback: {text}')

    if text == '/cancel':
        return cancel(update, context)

    context.bot.send_message(chat_id=int(TELEGRAM_ADMIN_ID),
                             text=f'Message from {chat_id}:\n{text}')
    log_command_in_db(COMMAND_NAME, chat_id, is_completed=True, is_cancelled=False)
    update.message.reply_text('Your message has been successfully received. Thank you!')
    return ConversationHandler.END


def cancel(update, context):
    log_command_in_db(COMMAND_NAME, update.message.chat_id, is_completed=False, is_cancelled=True)
    update.message.reply_text('Ok bye')
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('feedback', start)],
    states={
        States.FEEDBACK: [MessageHandler(Filters.text, feedback)],
        States.CANCEL: [MessageHandler(Filters.text, cancel)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
