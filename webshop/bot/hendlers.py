# -*- coding: utf-8 -*-
import os

from ..db import Category, Product, User, New, Text, Order
from .keyboards import START_KB
from .lookups import (SEPARATOR,
                      HENDLER_ORDER,
                      HENDLER_CATEGORY,
                      HENDLER_PRODUCT,
                      HENDLER_HISTORY_ORDER,
                      HENDLER_ADD_COUNT_PRODUCT,
                      HENDLER_SUB_COUNT_PRODUCT)
from .services import WebShopBot


bot_instance = WebShopBot(os.environ.get('TOKEN_KEY'))

# start
@bot_instance.message_handler(content_types=['text'], commands=['start'])
def start(message):
    user = User.get_user(chat=message.chat)
    text = Text.get_body(Text.GRITINGS)
    bot_instance.generate_and_send_start_kb(user, text)

# Список категорій
@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['categories'])
def get_categories(message):
    bot_instance.clear_messages_from_cart(message.chat)
    bot_instance.generate_and_send_categories_kb(Text.get_body(Text.LIST_CATEGORYS), message.chat.id, Category.get_root_categories())

# Товари із знижкою
@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['discount'])
def get_products_with_discount(message):
    bot_instance.clear_messages_from_cart(message.chat)
    bot_instance.send_products(message.chat.id, Product.get_products_with_discount())

# Вивести новини
@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['news'])
def get_news(message):
    bot_instance.clear_messages_from_cart(message.chat)
    bot_instance.send_news(message.chat.id, New.get_latest_news(3))

# Перейти в корзину
@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text.find(Text.get_body(Text.GO_TO_CART)) >= 0)
def go_to_cart(message):
    bot_instance.clear_messages_from_cart(message.chat)
    bot_instance.send_cart(message)

# Історія заказів
@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text.find(Text.get_body(Text.ORDER_HISTORY)) >= 0)
def order_hystory(message):
    bot_instance.clear_messages_from_cart(message.chat)
    user = User.get_user(chat=message.chat)
    bot_instance.get_history_orders(user)

#Ці перевірки повинні бути останніми
#Ввели номер телефона
@bot_instance.message_handler(content_types=['text'],
            func=lambda m: Order.get_active_order(User.get_user(chat=m.chat)).last_request == Order.REQUEST_TELEPHONE)
def set_telephone_user(message):
    user = User.get_user(chat=message.chat)
    bot_instance.set_telephone_user(user, message.text)

#Ввели ФІО
@bot_instance.message_handler(content_types=['text'],
            func=lambda m: Order.get_active_order(User.get_user(chat=m.chat)).last_request == Order.REQUEST_NAME)
def set_telephone_user(message):
    user = User.get_user(chat=message.chat)
    bot_instance.set_name_user(user, message.text)


# Клікнули по категорії
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HENDLER_CATEGORY)
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
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HENDLER_PRODUCT)
def clic_product(call):
    product = Product.objects.get(id=call.data.split(SEPARATOR)[1])
    user = User.get_user(chat=call.message.chat)
    # Треба додати діалог вводу кількості
    order = Order.get_active_order(user)
    order.add_product_to_order(product, 1)

    text = f'{product.title} - {Text.get_body(Text.PRODUCT_ADD_TO_CART)}'
    bot_instance.generate_and_send_start_kb(user, text)

# Клікнули Оформити замовлення
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HENDLER_ORDER
                                                       and call.data.split(SEPARATOR)[2] == Order.ORDER_PROCESSED)
def order_complete(call):
    order = Order.objects.get(id=call.data.split(SEPARATOR)[1])
    bot_instance.clear_messages_from_cart(call.message.chat)
    bot_instance.process_order(order, call.message.message_id)

# Клікнули Відмінити замовлення
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HENDLER_ORDER
                                     and call.data.split(SEPARATOR)[2] == Order.ORDER_CANCELED)
def order_canceled(call):
    order = Order.objects.get(id=call.data.split(SEPARATOR)[1])
    bot_instance.clear_messages_from_cart(call.message.chat)
    bot_instance.next_status_order(order,  Order.ORDER_CANCELED)

# Клікнули "Показать заказ"
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HENDLER_HISTORY_ORDER)
def show_order(call):
    order = Order.objects.get(id=call.data.split(SEPARATOR)[1])
    bot_instance.send_order(order)

# Клікнули "Додати кількість"
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HENDLER_ADD_COUNT_PRODUCT)
def show_order(call):
    order = Order.objects.get(id=call.data.split(SEPARATOR)[1])
    bot_instance.update_and_send_line_order(order, order.add_count_in_line, int(call.data.split(SEPARATOR)[2]),
                                            call.message.message_id)


# Клікнули "Зменшити кількість"
@bot_instance.callback_query_handler(func=lambda call: call.data.split(SEPARATOR)[0] == HENDLER_SUB_COUNT_PRODUCT)
def show_order(call):
    order = Order.objects.get(id=call.data.split(SEPARATOR)[1])
    bot_instance.update_and_send_line_order(order, order.sub_count_in_line, int(call.data.split(SEPARATOR)[2]),
                                            call.message.message_id)




