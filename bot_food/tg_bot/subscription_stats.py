import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


ATTEMPT_LIMIT = 3
SUBSCRIPTION_PRICE = 500
STATS_FILE = "subscription_stats.json"
SUBSCRIPTIONS_FILE = "user_subscriptions.json"


def load_subscriptions():
    """Загрузка данных о подписках пользователей."""
    try:
        with open(SUBSCRIPTIONS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_subscriptions(subscriptions):
    """Сохранение данных о подписках."""
    with open(SUBSCRIPTIONS_FILE, 'w', encoding='utf-8') as file:
        json.dump(subscriptions, file, indent=4, ensure_ascii=False)


def load_stats():
    """Загрузка статистики подписчиков."""
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'total_subscriptions': 0, 'total_revenue': 0}


def save_stats(stats: dict):
    """Сохранение обновленной статистики подписчиков."""
    with open(STATS_FILE, 'w', encoding='utf-8') as file:
        json.dump(stats, file, indent=4, ensure_ascii=False)


def add_subscription():
    """Обработка новой подписки."""
    stats = load_stats()
    stats['total_subscriptions'] += 1
    stats['total_revenue'] = stats['total_subscriptions'] * SUBSCRIPTION_PRICE
    save_stats(stats)


def get_total_subscriptions():
    """Возвращает общее число подписок."""
    stats = load_stats()
    return stats['total_subscriptions']


def get_total_revenue():
    """Возвращает общий доход от подписок."""
    stats = load_stats()
    return stats['total_revenue']


def subscribe(query, context):
    """
    открывает страницу оплаты подписки.
    """
    query.answer()

    payment_url = "https://visionary-starship-998050.netlify.app"

    keyboard = [
        [InlineKeyboardButton("Перейти к оплате", url=payment_url)],
        [InlineKeyboardButton("Я оплатил", callback_data='check_payment')],
        [InlineKeyboardButton("Назад", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "Оформление подписки\n\n"
        "Стоимость: 500 руб./месяц\n\n"
        "Демо-процесс:\n"
        "1. Нажмите «Перейти к оплате»\n"
        "2. Заполните форму данными:\n"
        "3. Нажмите «Оплатить»\n"
        "4. Вернитесь и нажмите «Я оплатил»\n"
        "5. Подписка активируется автоматически"
    )

    query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


def check_payment(query, context):
    """
    Проверка оплаты и активация подписки
    """
    query.answer()

    user_id = query.from_user.id

    # Активируем подписку в БД
    activate_user_subscription(user_id)

    # Активируем подписку в БД
    context.user_data['subscribed'] = True
    if 'attempts_left' in context.user_data:
        del context.user_data['attempts_left']

    add_subscription()

    keyboard = [
        [InlineKeyboardButton("Получить рецепт", callback_data='dish')],
        [InlineKeyboardButton("В меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="Поздравляем! Ваша подписка успешно активирована!\n\n"
             "Теперь вы можете получать неограниченное количество рецептов!",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


def activate_user_subscription(user_id):
    """Активирует подписку для пользователя навсегда."""
    subscriptions = load_subscriptions()

    subscriptions[str(user_id)] = {
        'active': True
    }

    save_subscriptions(subscriptions)


def check_subscription(context, user_id=None):
    """Проверяет, есть ли у пользователя активная подписка"""
    if context.user_data.get('subscribed'):
        return True

    if user_id is None:
        return False

    return check_user_subscription(user_id)


def check_user_subscription(user_id):
    """Проверяет подписку пользователя в постоянном хранилище."""
    try:
        subscriptions = load_subscriptions()

        if str(user_id) not in subscriptions:
            return False

        sub_data = subscriptions[str(user_id)]

        return sub_data.get('active', False)

    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False
