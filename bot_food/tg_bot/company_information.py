from telegram import Update, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackContext 


def info(query: Update, context: CallbackContext):
    """Отправляет информацию о команде и кнопку возврата в меню."""
    query.answer()
    
    text = (
        "Команда Романа и Ларисы — это творческий дуэт увлечённых кулинаров, чья страсть к приготовлению вкусных блюд нашла отражение в обширной библиотеке рецептов в Instagram.\n"
        "За годы своего существования они собрали внушительную коллекцию кулинарных идей,\n"
        "каждая из которых отличается оригинальностью и простотой исполнения.",
    )
    
    keyboard = [
        [InlineKeyboardButton("В меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard) 
    
    query.edit_message_text(
        text=text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
