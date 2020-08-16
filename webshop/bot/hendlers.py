from telebot.types import (
    KeyboardButton,
    ReplyKeyboardMarkup)

from .config import TOKEN
from ..db import Category, Product, User, New, Text
from .keyboards import START_KB, ADD_TO_CART
from .lookups import SEPARATOR
from .services import WebShopBot


bot_instance = WebShopBot(TOKEN)


@bot_instance.message_handler(content_types=['text'], commands=['start'])
def start(message):
    print(message.chat)
    user = User.get_user(chat=message.chat)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(button) for button in START_KB.values()]
    kb.add(*buttons)
    txt = Text.objects.get(title=Text.GRITINGS).body
    bot_instance.send_message(message.chat.id, txt, reply_markup=kb)

@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['categories'])
def get_categories(message):
    bot_instance.generate_and_send_categories_kb('Список категорий', message.chat.id, Category.get_root_categories())

@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['discount'])
def get_products_with_discount(message):
    bot_instance.send_products(message.chat.id, Product.get_products_with_discount())

@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['news'])
def get_news(message):
    bot_instance.send_news(message.chat.id, New.get_latest_news(3))

# Клікнули по категорії
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == Category.__name__)
def clic_category(call):
    id_category = call.data.split(SEPARATOR)[1]
    print(9999999999999999, id_category)

    if id_category != 'None':
        category = Category.objects.get(id=call.data.split(SEPARATOR)[1])
        subcategories = list(category.subcategories)
        if subcategories:
            subcategories.append(category.parent)
        title_ = category.title
    else:
        subcategories = Category.get_root_categories()
        title_ = 'Список категорий'

    print(subcategories)

    if subcategories:
        bot_instance.generate_and_edit_categories_kb(title_, call.message.chat.id, call.message.message_id,
                                                  subcategories)
    else:
        # Вивести список товарів
        bot_instance.send_products(call.message.chat.id, category.get_products())


# Клікнули по товару
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == Product.__name__)
def clic_product(call):
    product = Product.objects.get(id=call.data.split(SEPARATOR)[1])
    # bot_instance.edit_message_text(product.title, call.message.chat.id, call.message.message_id)
    print('Не реализовано')

