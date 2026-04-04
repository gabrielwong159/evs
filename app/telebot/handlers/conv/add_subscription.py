from enum import Enum

from telegram import ChatAction
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from app.clients.db import DbClient
from app.clients.evs import EvsClient
from app.models.exception import LoginError
from app.services.account import AccountService
from app.services.subscription import SubscriptionService
from app.telebot.handlers.logging import logger, log_command_in_db

COMMAND_NAME = 'add_subscription'


class States(Enum):
    USERNAME, PASSWORD, AMOUNT = range(3)


def start(update, context):
    update.message.reply_text('Create a new subscription to receive notifications '
                              'when your credit balance falls below a preset amount.\n\n'
                              'First, I will need your EVS login credentials. '
                              'Begin by entering your username. (20000xxx)')
    return States.USERNAME


def username(update, context):
    context.chat_data['username'] = update.message.text
    logger.info(f'({update.message.chat_id}) Add subscription - username: {context.chat_data["username"]}')
    update.message.reply_text('Now enter your password, and I will validate your credentials.\n\n'
                              'Type /cancel at any time to leave this conversation.')
    return States.PASSWORD


def password(update, context):
    chat_id = update.message.chat_id
    pw = update.message.text
    context.chat_data['password'] = pw
    logger.info(f'({chat_id}) Add subscription - password: {pw}')

    if pw == '/cancel':
        log_command_in_db(COMMAND_NAME, chat_id, is_completed=False, is_cancelled=True)
        update.message.reply_text('Ok bye')
        return ConversationHandler.END

    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    uname = context.chat_data['username']
    try:
        valid = EvsClient().login(uname, pw)
    except Exception:
        update.message.reply_text('Sorry, but we have faced a connection error while validating your credentials. '
                                  'Please try again in a few minutes.')
        return ConversationHandler.END

    if valid:
        AccountService(DbClient()).insert_account(uname, pw)
        logger.info(f'({chat_id}) Add subscription - account added')
        update.message.reply_text('Finally, enter the notification amount. '
                                  'You will receive a message when your credit balance falls below this amount.')
        return States.AMOUNT
    else:
        update.message.reply_text(f'Could not login. Enter your password for account {uname}.\n\n'
                                  'Type /cancel at any time to leave this conversation.')
        return States.PASSWORD


def amount(update, context):
    text = update.message.text
    try:
        amt = round(float(text), 2)
    except ValueError:
        update.message.reply_text('Could not convert amount to float. Please enter amount again.')
        return States.AMOUNT

    uname = context.chat_data['username']
    chat_id = update.message.chat.id

    SubscriptionService(DbClient()).insert_subscription(uname, amt, chat_id)
    logger.info(f'({chat_id}) Add subscription - subscription added: ({uname}, {amt}, {chat_id})')
    log_command_in_db(COMMAND_NAME, chat_id, is_completed=True, is_cancelled=False)
    update.message.reply_text(f'Your subscription has been successfully added: {uname} - ${amt:.2f}\n\n'
                              f'Use /view to view and delete your subscriptions.')
    return ConversationHandler.END


def cancel(update, context):
    log_command_in_db(COMMAND_NAME, update.message.chat_id, is_completed=False, is_cancelled=True)
    update.message.reply_text('Ok bye')
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', start)],
    states={
        States.USERNAME: [MessageHandler(Filters.text, username)],
        States.PASSWORD: [MessageHandler(Filters.text, password)],
        States.AMOUNT: [MessageHandler(Filters.text, amount)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
