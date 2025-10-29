from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import random
import logging
import os
from demo_data.demo_db import data
from tg_bot.subscription_stats import check_subscription


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def dish(query: Update, context: CallbackContext):
    """Показывает случайное блюдо."""
    subscribed = context.user_data.get('subscribed', False)

    if subscribed:
        all_dishes = data.copy()
        chosen_dish_key = random.choice(list(all_dishes.keys()))
        chosen_dish = all_dishes[chosen_dish_key]

        context.user_data['current_dish'] = chosen_dish

        relative_image_path = chosen_dish["Image"]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_folder = os.path.join(base_dir, "..", "demo_data", "images")
        absolute_image_path = os.path.join(images_folder, os.path.basename(relative_image_path))

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
        attempts_left = context.user_data.get('attempts_left', 0)

        if attempts_left > 0:
            context.user_data['attempts_left'] -= 1

            all_dishes = data.copy()
            chosen_dish_key = random.choice(list(all_dishes.keys()))
            chosen_dish = all_dishes[chosen_dish_key]

            context.user_data['current_dish'] = chosen_dish

            relative_image_path = chosen_dish["Image"]
            base_dir = os.path.dirname(os.path.abspath(__file__))
            images_folder = os.path.join(base_dir, "..", "demo_data", "images")
            absolute_image_path = os.path.join(images_folder, os.path.basename(relative_image_path))

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
            offer_subscription(query, context)


def show_recipe(query: Update, context: CallbackContext):
    """Показывает рецепт текущего блюда."""
    current_dish = context.user_data.get('current_dish')

    ingredients = '\n'.join(current_dish['products'])
    recipe_steps = current_dish['recipe']
    message_text = (
        f"*{current_dish['Name']}* 📖 Рецепт\n\n"
        f"*Ингредиенты:*\n{ingredients}\n\n"
        f"*Пошагово:*\n{recipe_steps}"
    )

    buttons = [[InlineKeyboardButton("Следующее блюдо", callback_data='next_dish')]]
    reply_markup = InlineKeyboardMarkup(buttons)

    query.message.reply_text(
        text=message_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


def offer_subscription(update: Update, context: CallbackContext):
    """Предлагает оформить подписку после исчерпания бесплатных попыток."""
    keyboard = [
        [InlineKeyboardButton("Оформить подписку", callback_data='subscribe')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Ваши бесплатные попытки закончились.\n"
        "Оформите подписку, чтобы продолжить получать рецепты.",
        reply_markup=reply_markup
    )

