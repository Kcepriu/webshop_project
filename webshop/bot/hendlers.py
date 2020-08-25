from telebot.types import (
    KeyboardButton,
    ReplyKeyboardMarkup)

from .config import TOKEN
from ..db import Category, Product, User, New, Text
from .keyboards import START_KB
from .lookups import SEPARATOR
from .services import WebShopBot


bot_instance = WebShopBot(TOKEN)


@bot_instance.message_handler(content_types=['text'], commands=['start'])
def start(message):
    user = User.get_user(chat=message.chat)
    txt = Text.get_body(Text.GRITINGS)
    bot_instance.update_keyboard_markup(user, message.chat.id, txt)

@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['categories'])
def get_categories(message):
    bot_instance.generate_and_send_categories_kb(Text.get_body(Text.LIST_CATEGORYS), message.chat.id, Category.get_root_categories())

@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['discount'])
def get_products_with_discount(message):
    bot_instance.send_products(message.chat.id, Product.get_products_with_discount())

@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['news'])
def get_news(message):
    bot_instance.send_news(message.chat.id, New.get_latest_news(3))

@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == Text.get_body(Text.GO_TO_CART))
def go_to_cart(message):
    pass

@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == Text.get_body(Text.ORDER_HYSTORY))
def order_hystory(message):
    pass


# Клікнули по категорії
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == Category.__name__)
def clic_category(call):
    id_category = call.data.split(SEPARATOR)[1]

    if id_category != 'None':
        category = Category.objects.get(id=call.data.split(SEPARATOR)[1])
        subcategories = list(category.subcategories)
        if subcategories:
            subcategories.append(category.parent)
        title_ = category.title
    else:
        subcategories = Category.get_root_categories()
        title_ = Text.get_body(Text.LIST_CATEGORYS)

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
    user = User.get_user(chat=call.message.chat)
    # Треба додати діалог вводу кількості
    user.add_product_to_order(product, 1)
    txt = Text.get_body(Text.PRODUCT_ADD_TO_CART)
    bot_instance.update_keyboard_markup(user, call.message.chat.id, txt)

