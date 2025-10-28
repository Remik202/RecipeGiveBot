from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import random
import logging 
import os 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

from demo_data.demo_db import data 

def dish(query: Update, context: CallbackContext):
    # Проверка подписки - Добавил еще код (Антон)
    from tg_bot.subscription_stats import check_subscription
    # Сначала проверяем наличие подписки
    subscribed = context.user_data.get('subscribed', False)

    if subscribed:
        # Если пользователь оформил подписку, показываем случайное блюдо без учета попыток
        all_dishes = data.copy()
        chosen_dish_key = random.choice(list(all_dishes.keys()))
        chosen_dish = all_dishes[chosen_dish_key]
        
        # Сохраняем текущее блюдо
        context.user_data['current_dish'] = chosen_dish

        # Отправляем фотографию блюда
        relative_image_path = chosen_dish["Image"]
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        IMAGES_FOLDER = os.path.join(BASE_DIR, "..", "demo_data", "images")
        absolute_image_path = os.path.join(IMAGES_FOLDER, os.path.basename(relative_image_path))

        # Формируем текст и кнопки
        message_text = f"🍽️ Ваше блюдо: *{chosen_dish['Name']}*"
        buttons = [
            [
                InlineKeyboardButton("Следующее блюдо", callback_data='next_dish'),
                InlineKeyboardButton("Показать рецепт", callback_data='show_recipe')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        with open(absolute_image_path, 'rb') as photo_file:
            context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=photo_file,
                caption=message_text,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
    else:
        # Проверяем оставшиеся бесплатные попытки
        attempts_left = context.user_data.get('attempts_left', 0)

        if attempts_left > 0:
            # Если у пользователя остались бесплатные попытки, уменьшаем счётчик
            context.user_data['attempts_left'] -= 1

            # Остальной код остается прежним
            all_dishes = data.copy()
            chosen_dish_key = random.choice(list(all_dishes.keys()))
            chosen_dish = all_dishes[chosen_dish_key]
            
            # Сохраняем текущее блюдо
            context.user_data['current_dish'] = chosen_dish

            # Отправляем фотографию блюда
            relative_image_path = chosen_dish["Image"]
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            IMAGES_FOLDER = os.path.join(BASE_DIR, "..", "demo_data", "images")
            absolute_image_path = os.path.join(IMAGES_FOLDER, os.path.basename(relative_image_path))

            # Формируем текст и кнопки
            message_text = f"🍽️ Ваше блюдо: *{chosen_dish['Name']}*"
            buttons = [
                [
                    InlineKeyboardButton("Следующее блюдо", callback_data='next_dish'),
                    InlineKeyboardButton("Показать рецепт", callback_data='show_recipe')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)

            with open(absolute_image_path, 'rb') as photo_file:
                context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=photo_file,
                    caption=message_text,
                    parse_mode="Markdown",
                    reply_markup=reply_markup
                )
        else:
            # Предложение оформить подписку
            offer_subscription(query, context)

# Функция отображения рецепта
def show_recipe(query: Update, context: CallbackContext):
    current_dish = context.user_data.get('current_dish')

    # Формируем сообщение с рецептом
    ingredients = '\n'.join(current_dish['products'])
    recipe_steps = current_dish['recipe']
    message_text = f"**{current_dish['Name']}** 📖 Рецепт\n\n"
    message_text += f"Ингредиенты:\n{ingredients}\n\n"
    message_text += f"Пошагово:\n{recipe_steps}"

    # Кнопка для следующего блюда
    buttons = [[InlineKeyboardButton("Следующее блюдо", callback_data='next_dish')]]
    reply_markup = InlineKeyboardMarkup(buttons)

    query.message.reply_text(
        text=message_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# Функция оферты подписки
def offer_subscription(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Оформить подписку", callback_data='subscribe')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Ваши бесплатные попытки закончились. Оформите подписку, чтобы продолжить получать рецепты.",
                              reply_markup=reply_markup)