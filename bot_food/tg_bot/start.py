from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

ATTEMPT_LIMIT = 3  # Максимальное число попыток
SUBSCRIBED = False  # Флаг подписки


def start(update: Update, context: CallbackContext): 
  """Обработчик команды /start — приветственное сообщение и главное меню."""
    context.user_data['attempts_left'] = ATTEMPT_LIMIT
    context.user_data['subscribed'] = False
    update.message.reply_text("Добро пожаловать в FoodPlanner!\n\n"
                              "Это кулинарный бот.\n"
                              "Здесь вы найдете вкусные рецепты и сможете готовить как шеф-повар .\n"
                              "Начнем?\n\n")
    keyboard = [
        [
            InlineKeyboardButton("Случайное блюдо", callback_data='dish'),
            InlineKeyboardButton("Офорить подписку",
                                 callback_data='subscribe'),
        ],
        [InlineKeyboardButton("О нас", callback_data='info'),
         InlineKeyboardButton("Оплаченных подписок",
                              callback_data='statistics')
         ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Пожалуйста, выберите:',
                              reply_markup=reply_markup)


