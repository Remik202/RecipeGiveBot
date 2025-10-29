from demo_data.demo_db import data
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import random
import logging
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def dish(query: Update, context: CallbackContext):
    # Получаем ID пользователя
    if query.message:
        user_id = query.message.from_user.id
    elif query.callback_query:
        user_id = query.callback_query.from_user.id
    else:
        user_id = None

    # Проверяем подписку через функцию
    from tg_bot.subscription_stats import check_subscription
    subscribed = check_subscription(context, user_id)
    context.user_data[user_id] = subscribed

    if subscribed:
        # Код для пользователь с подпиской
        all_dishes = data.copy()

        shuffled_keys = context.user_data.get('shuffled_keys', None)
        if shuffled_keys is None:

            shuffled_keys = list(all_dishes.keys())
            random.shuffle(shuffled_keys)
            context.user_data['shuffled_keys'] = shuffled_keys

        if len(shuffled_keys) == 0:

            shuffled_keys = list(all_dishes.keys())
            random.shuffle(shuffled_keys)
            context.user_data['shuffled_keys'] = shuffled_keys

        chosen_dish_key = shuffled_keys.pop()
        chosen_dish = all_dishes[chosen_dish_key]

        context.user_data['current_dish'] = chosen_dish

        relative_image_path = chosen_dish["Image"]
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        IMAGES_FOLDER = os.path.join(BASE_DIR, "..", "demo_data", "images")
        absolute_image_path = os.path.join(
            IMAGES_FOLDER, os.path.basename(relative_image_path)
        )

        message_text = f"🍽️ Ваше блюдо: *{chosen_dish['Name']}*"
        buttons = [
            [
                InlineKeyboardButton(
                    "Следующее блюдо", callback_data='next_dish'
                ),
                InlineKeyboardButton(
                    "Показать рецепт", callback_data='show_recipe'
                )
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
        # Код для пользователей не имеющих подписку
        attempts_left = context.user_data.get('attempts_left', 3)

        if attempts_left > 0:

            context.user_data['attempts_left'] -= 1

            all_dishes = data.copy()

            shuffled_keys = context.user_data.get('shuffled_keys', None)
            if shuffled_keys is None:

                shuffled_keys = list(all_dishes.keys())
                random.shuffle(shuffled_keys)
                context.user_data['shuffled_keys'] = shuffled_keys

            if len(shuffled_keys) == 0:

                shuffled_keys = list(all_dishes.keys())
                random.shuffle(shuffled_keys)
                context.user_data['shuffled_keys'] = shuffled_keys

            chosen_dish_key = shuffled_keys.pop()
            chosen_dish = all_dishes[chosen_dish_key]

            context.user_data['current_dish'] = chosen_dish

            relative_image_path = chosen_dish["Image"]
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            IMAGES_FOLDER = os.path.join(BASE_DIR, "..", "demo_data", "images")
            absolute_image_path = os.path.join(
                IMAGES_FOLDER, os.path.basename(relative_image_path))

            message_text = f"🍽️ Ваше блюдо: *{chosen_dish['Name']}*"
            buttons = [
                [
                    InlineKeyboardButton(
                        "Следующее блюдо", callback_data='next_dish'),
                    InlineKeyboardButton(
                        "Показать рецепт", callback_data='show_recipe')
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


def show_recipe(query: Update, context: CallbackContext):
    # Функция отображения рецепта
    current_dish = context.user_data.get('current_dish')

    if not current_dish:
        query.message.reply_text("Сначала выберите блюдо!")
        return

    ingredients = '\n'.join(current_dish['products'])
    recipe_steps = current_dish['recipe']
    message_text = f"**{current_dish['Name']}** 📖 Рецепт\n\n"
    message_text += f"Ингредиенты:\n{ingredients}\n\n"
    message_text += f"Пошагово:\n{recipe_steps}"

    buttons = [[InlineKeyboardButton(
        "Следующее блюдо", callback_data='next_dish')]]
    reply_markup = InlineKeyboardMarkup(buttons)

    query.message.reply_text(
        text=message_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


def offer_subscription(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Оформить подписку", callback_data='subscribe')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if hasattr(update, 'callback_query'):
        update.callback_query.message.reply_text(
            "Ваши бесплатные попытки закончились.\n\n"
            "Оформите подписку, чтобы продолжить получать рецепты.",
            reply_markup=reply_markup)
    else:
        update.message.reply_text(
            "Ваши бесплатные попытки закончились.\n\n"
            "Оформите подписку, чтобы продолжить получать рецепты.",
            reply_markup=reply_markup)
