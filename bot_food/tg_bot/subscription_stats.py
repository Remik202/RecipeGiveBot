import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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

def subscribe(update, context):
    """
    Обработчик подписки. Регистрирует нового подписчика и увеличивает статистику.
    """
    

    # Установка статуса пользователя как подписавшегося
    context.user_data['subscribed'] = True
    context.user_data['attempts_left'] = ATTEMPT_LIMIT  # Используем глобальное значение ATTEMPT_LIMIT
    
    if 'attempts_left' in context.user_data:
        del context.user_data['attempts_left']

    keyboard = [
        [InlineKeyboardButton("В меню ", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Увеличение общей статистики подписок
    add_subscription()

    # Отправляем сообщение пользователю
    update.edit_message_text(text="Поздравляем! Ваша подписка успешно активирована.",reply_markup=reply_markup) 
    