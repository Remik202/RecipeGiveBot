from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

ATTEMPT_LIMIT = 3  # Максимальное число попыток


def start(update: Update, context: CallbackContext):
    """Обработчик команды /start — приветственное сообщение и главное меню."""
    if update.message:
        user_id = update.message.from_user.id
    elif update.callback_query:
        user_id = update.callback_query.from_user.id
    else:
        user_id = None

    if 'attempts_left' not in context.user_data:
        context.user_data['attempts_left'] = ATTEMPT_LIMIT

    # Проверка подписки
    from tg_bot.subscription_stats import check_subscription
    subscribed = check_subscription(
        context, user_id)  # Исправлено имя переменной
    context.user_data['subscribed'] = subscribed  # Исправлено имя ключа

    if subscribed:
        # Меню для подписанных пользователей
        welcome_text = (
            "Добро пожаловать в FoodPlanner!\n\n"
            "У вас активная подписка!\n\n"
            "Вы можете получать неограниченное количество рецептов.\n\n"
            "Выберите действие:")

        keyboard = [
            [
                InlineKeyboardButton("Случайное блюдо", callback_data='dish'),
                InlineKeyboardButton("О нас", callback_data='info')
            ],
            [
                InlineKeyboardButton(
                    "Статистика подписок", callback_data='statistics'
                )
            ]
        ]
    else:
        # Меню для пользователей не имеющих подписки
        # Исправлено на user_data
        attempts_left = context.user_data['attempts_left']
        welcome_text = (
            f"Добро пожаловать в FoodPlanner!\n\n"
            f"Это кулинарный бот.\n\n"
            f"Здесь вы найдете вкусные рецепты \n\n"
            f"и сможете готовить как шеф-повар.\n\n"
            f"Бесплатных попыток осталось: {attempts_left}\n\n"
            f"Выберите действие:")
        keyboard = [
            [
                InlineKeyboardButton("Случайное блюдо", callback_data='dish'),
                InlineKeyboardButton("Оформить подписку", callback_data='subscribe')
            ],
            [
                InlineKeyboardButton("О нас", callback_data='info'),
                InlineKeyboardButton("Статистика", callback_data='statistics')
            ]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        update.message.reply_text(welcome_text, reply_markup=reply_markup)
    else:
        update.callback_query.message.reply_text(
            welcome_text, reply_markup=reply_markup)
