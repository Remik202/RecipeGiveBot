import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def statistics(file_path, key):

    if not os.path.exists(file_path):
        return "Подписок еще нет!"

    with open(file_path, 'r') as file:
        data = json.load(file)

    if key in data:
        value = data.get(key)
        return f"Количество подписок {value}"
    else:
        print(f'Ошибка: Ключ "{key}" не найден.')


def statistics_bot(query: Update, context: CallbackContext):
    file_name = 'subscription_stats.json'
    result = statistics(file_name, 'total_subscriptions')
    print(result)
    query.answer()

    query.edit_message_text(text=result, parse_mode='Markdown')

    keyboard = [

        [InlineKeyboardButton("В меню", callback_data='start')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_reply_markup(reply_markup=reply_markup)
