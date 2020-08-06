from telebot.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton)
from telebot import TeleBot

from .config import TOKEN
from db.models import Category, Product, Parameter, New
from .keyboards import START_KB
from .texts import TEXTS, SEPARATOR


bot = TeleBot(TOKEN)

def send_message(id, message):
    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            bot.send_message(id, message[x:x + 4096])
    else:
        bot.send_message(id, message)


@bot.message_handler(content_types=['text'], commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(button) for button in START_KB.values()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, TEXTS.get('make_selection', ''), reply_markup=kb)

@bot.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['list_categories'])
def list_categories(message):
    buttons = [
        InlineKeyboardButton(
            category.title,
            callback_data=f'{Category.__name__}{SEPARATOR}{str(category.id)}'
        )  for category in Category.get_root_categories()
    ]

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(*buttons)
    bot.send_message(message.chat.id, TEXTS['list_categories'], reply_markup=kb)

@bot.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['list_products_with_discount'])
def list_products_with_discount(message):
    buttons = [
        InlineKeyboardButton(
            product.title,
            callback_data=f'{Product.__name__}{SEPARATOR}{str(product.id)}'
        ) for product in Product.get_products_with_discount()
    ]

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(*buttons)
    bot.send_message(message.chat.id, TEXTS['list_products_with_discount'], reply_markup=kb)


@bot.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['list_news'])
def list_news(message):
    news = New.get_latest_news(3)
    for item in news:
        send_message(message.chat.id, item.title)
        send_message(message.chat.id, item.text)

@bot.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == Category.__name__)
def clic_category(call):
    category = Category.objects.get(id=call.data.split(SEPARATOR)[1])
    buttons = []

    if not category.parent is None:
        buttons.append(InlineKeyboardButton(
            f'Вернутся {category.parent.title}',
            callback_data=f'{Category.__name__}{SEPARATOR}{str(category.parent.id)}'))

    for subcategory in category.subcategories:
        buttons.append(InlineKeyboardButton(
            f'Перейти {subcategory.title}',
            callback_data=f'{Category.__name__}{SEPARATOR}{str(subcategory.id)}'))

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(*buttons)

    bot.edit_message_text(category.title, call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == Product.__name__)
def clic_product(call):
    product = Product.objects.get(id=call.data.split(SEPARATOR)[1])
    bot.edit_message_text(product.title, call.message.chat.id, call.message.message_id)
