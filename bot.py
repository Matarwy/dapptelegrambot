import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
    CallbackContext,
    CallbackQueryHandler
)
from utlis.handlers import *
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
persistence = PicklePersistence(filename="conversationbot/conversationbot")
updater = Updater(token=BOT_TOKEN, use_context=True, persistence=persistence)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start)
    ],
    states={
        MAIN: [
            MessageHandler(Filters.text, Main)
        ],
        SET_ADDRESS: [
            MessageHandler(Filters.regex("^0x[a-fA-F0-9]{40}$"), setWallet),
            MessageHandler(Filters.regex("^Cancel$"), cancel)
        ],
    },
    fallbacks=[],
    name="main",
    persistent=True,
    per_user=True
)


def handle_callback_query(update, context):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id


callback_query_handler = CallbackQueryHandler(handle_callback_query)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(callback_query_handler)

updater.start_polling()
