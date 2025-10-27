from telegram import Update, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackContext 

def info(query: Update, context: CallbackContext):
    
    query.answer()
    
    query.edit_message_text(
        text="Команда Романа и Ларисы — это творческий дуэт увлечённых кулинаров, чья страсть к приготовлению вкусных блюд нашла отражение в обширной библиотеке рецептов в Instagram.\n"
             "За годы своего существования они собрали внушительную коллекцию кулинарных идей,\n"
             "каждая из которых отличается оригинальностью и простотой исполнения.",
        parse_mode='Markdown'
    )
    keyboard = [ 
       
    [InlineKeyboardButton("В меню", callback_data='start')],
    ] 
    reply_markup = InlineKeyboardMarkup(keyboard) 
    query.edit_message_reply_markup(reply_markup=reply_markup)