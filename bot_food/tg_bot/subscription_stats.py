import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
# Глобальная константа ограничения попыток
ATTEMPT_LIMIT = 3

# Остальные части кода остаются прежними
SUBSCRIPTION_PRICE = 500
STATS_FILE = "subscription_stats.json"

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
    query.answer()  # Подтверждаем нажатие кнопки

    payment_url = "https://visionary-starship-998050.netlify.app"

    keyboard = [
        [InlineKeyboardButton("Перейти к оплате", url=payment_url)],
        [InlineKeyboardButton("Я оплатил", callback_data='check_payment')],
        [InlineKeyboardButton("Назад", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="Оформление подписки\n\n"
             "Стоимость: 500 руб./месяц\n\n"
             "Демо-процесс:\n"
             "1. Нажмите «Перейти к оплате»\n"
             "2. Заполните форму данными:\n"
             "3. Нажмите «Отправить»\n"
             "4. Вернитесь и нажмите «Я оплатил»\n"
             "5. Подписка активируется автоматически",
        reply_markup=reply_markup
    )

def check_payment(query, context):
    """
    Проверка оплаты и активация подписки
    """
    query.answer()

    # Активируем подписку
    context.user_data['subscribed'] = True

    # if 'attempts_left' in context.user_data:
    #     del context.user_data['attempts_left']

    add_subscription()

    keyboard = [
        [InlineKeyboardButton("Получить рецепт", callback_data='dish')],
        [InlineKeyboardButton("В меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="Поздравляем! Ваша подписка успешно активирована!\n\n"
             "Теперь вы можете получать неограниченное количество рецептов!",
        reply_markup=reply_markup
    )


def check_subscription(context, user_id=None):
    """Проверяет, есть ли у пользователя активная подписка"""
    return context.user_data.get('subscribed', False)
    