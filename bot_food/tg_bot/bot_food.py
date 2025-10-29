import os
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
from tg_bot.start import *
from tg_bot.recipes import dish, show_recipe
from tg_bot.subscription_stats import subscribe, check_payment
from tg_bot.company_information import info
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
BOT_TOKEN = os.getenv("RECIPE_GIVE_BOT")


def handle_button_click(update, context):
    """Обработчик нажатия на кнопку"""
    query = update.callback_query
    data = query.data

    if data == 'dish':
        dish(query, context)
    elif data == 'info':
        info(query, context)
    elif data == "start":
        start(query, context)
    elif query.data == 'next_dish':
        dish(query, context)
    elif query.data == 'show_recipe':
        show_recipe(query, context)
    elif query.data == 'subscribe':
        subscribe(query, context)
    elif data == 'check_payment':
        check_payment(query, context)


def main():
    """Запуск Telegram-бота"""
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("dish", dish))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("show_recipe", show_recipe))
    dispatcher.add_handler(CallbackQueryHandler(handle_button_click))
    
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()



