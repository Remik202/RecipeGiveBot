from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext 
import logging 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

ATTEMPT_LIMIT = 3  # Максимальное число попыток
SUBSCRIBED = False  # Флаг подписки

def start(update:Update, context: CallbackContext):  
    context.user_data['attempts_left'] = ATTEMPT_LIMIT
    context.user_data['subscribed'] = False
    update.message.reply_text("Добро пожаловать в FoodPlanner!\n\n" 
        "Это кулинарный бот.\n"
        "Здесь вы найдете вкусные рецепты и сможете готовить как шеф-повар .\n"
        "Начнем?\n\n") 
    keyboard = [ 
        [
            InlineKeyboardButton("Случайное блюдо", callback_data='dish'),
            InlineKeyboardButton("Офорить подписку", callback_data='subscribe'),
        ],
        [InlineKeyboardButton("О нас", callback_data='info')],
    ] 
    reply_markup = InlineKeyboardMarkup(keyboard) 
    update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup) 

# def button(update:Update, context:CallbackContext):
#     query = update.callback_query 
#     query.answer() 

#     if query.data == 'dish':  # Нажата кнопка "Случайное блюдо"
#         from tg_bot.recipes import dish
#         dish(query, context)
#     elif query.data == 'subscriptions':
#         query.edit_message_text(text="Вы выбрали оформить подписку.")
#     elif query.data == 'info': 
#         from tg_bot.company_information import info
#         info(query, context) 
    
        