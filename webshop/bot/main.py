from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton)
from telebot import TeleBot

from .config import TOKEN

from db.models import Category, Product, Parameter


bot = TeleBot(TOKEN)

@bot.message_handler(content_types=['text'], commands=['start'])
def start(message):
    buttons = [
        InlineKeyboardButton(
            category.title,
            callback_data=str(category.id)
        )  for category in Category.objects(parent=None)
    ]

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(*buttons)
    bot.send_message(message.chat.id, f'Категории', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def clic_item(call):
    pass


