from typing import List, Union
from telebot import TeleBot
from telebot.apihelper import ApiException
from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove,
                           KeyboardButton)
from mongoengine.errors import ValidationError

from ..db import Category, Product, New, Text, Order, User
from .lookups import (SEPARATOR,
                      HENDLER_ORDER,
                      HENDLER_CATEGORY,
                      HENDLER_PRODUCT,
                      HENDLER_HISTORY_ORDER,
                      HENDLER_SUB_COUNT_PRODUCT,
                      HENDLER_ADD_COUNT_PRODUCT)
from .config import NO_PHOTO_URL
from .keyboards import START_KB


class WebShopBot(TeleBot):
    def generety_categories_kb(self, categories: List[Union[Category, None]], **kwargs):
        kb = InlineKeyboardMarkup(**kwargs)
        buttons = []
        for category in categories:
            id_ = category.id if category else None
            title_ = category.title if category else Text.get_body(Text.RETURN_TO_TOP)

            buttons.append(InlineKeyboardButton(
                title_,
                callback_data=f'{HENDLER_CATEGORY}{SEPARATOR}{id_}'))

        kb.add(*buttons)
        return kb

    def generate_and_send_categories_kb(self, text: str, chat_id: int, categories: List[Category], **kwargs):
        self.send_message(chat_id, text, reply_markup=self.generety_categories_kb(categories, **kwargs))

    def generate_and_edit_categories_kb(self, text: str, chat_id: int, message_id: int,
                                        categories: List[Union[Category, None]], **kwargs):
        kb = self.generety_categories_kb(categories, **kwargs)
        self.edit_message_text(text, chat_id, message_id, reply_markup=kb)

    def send_products(self, chat_id: int, products: List[Product]):
        for product in products:
            kb = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text=Text.get_body(Text.ADD_TO_CART),
                                          callback_data=f'{HENDLER_PRODUCT}{SEPARATOR}{product.id}')
            kb.add(button)
            description = f'{product.description}\n{Text.get_body(Text.PRICE)}: {product.actual_price}'
            self.send_photo(chat_id, product.url_photo if product.url_photo else NO_PHOTO_URL,
                            description, reply_markup=kb)

    def send_long_message(self, id, message):
        if len(message) > 4096:
            for x in range(0, len(message), 4096):
                self.send_message(id, message[x:x + 4096])
        else:
            self.send_message(id, message)

    def send_news(self, chat_id: int, news: List[New]):
        for item in news:
            self.send_long_message(chat_id, item.title)
            self.send_long_message(chat_id, item.text)

    def generate_start_kb(self, user: User):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [KeyboardButton(button) for button in START_KB.values()]

        # Якщо в корзині є товар то додамо кнопку для виклику корзини
        count_products_from_cart = Order.get_count_products_in_active_order(user)
        if count_products_from_cart:
            buttons.append(KeyboardButton(f'{Text.get_body(Text.GO_TO_CART)} ({count_products_from_cart})'))

        # Якщо є раніше створені закази, то додамо кнопку для виклику історії заказів
        count_orders = Order.get_count_orders(user)
        if count_orders:
            buttons.append(KeyboardButton(f'{Text.get_body(Text.ORDER_HISTORY)} ({count_orders})'))

        kb.add(*buttons)
        return kb

    def generate_and_send_start_kb(self, user: User, text: str):
        kb = self.generate_start_kb(user)
        result = self.send_message(user.user_id, text, reply_markup=kb)

        return result.message_id

    def clear_messages_from_cart(self, chat: str):
        user = User.get_user(chat=chat)
        order = Order.find_active_order(user)
        if order:
            self.delete_message_from_cart(order)

    def delete_message_from_cart(self, order: Order):
        if not order.id_message_cart:
            return

        for message_id in order.id_message_cart:
            try:
                self.delete_message(order.user.user_id, message_id)
            except  ApiException:
                break
        order.id_message_cart = []
        order.save()

    def generate_kb_product_cart(self, order: Order, nom_line: int):
        kb_product = InlineKeyboardMarkup()
        button_product = []
        button_product.append(InlineKeyboardButton(text=Text.get_body(Text.SUB_COUNT),
                            callback_data=f'{HENDLER_SUB_COUNT_PRODUCT}{SEPARATOR}{order.id}{SEPARATOR}{nom_line}'))
        button_product.append(InlineKeyboardButton(text=Text.get_body(Text.ADD_COUNT),
                            callback_data=f'{HENDLER_ADD_COUNT_PRODUCT}{SEPARATOR}{order.id}{SEPARATOR}{nom_line}'))
        kb_product.add(*button_product)

        return kb_product

    def update_and_send_line_order(self, order: Order, func, num_line: int, message_id: int):
        func(num_line)
        order.reload()
        line_product = order.products[num_line]
        self.send_line_product_cart(order, line_product, num_line+1, message_id)
        self.send_footer_cart(order, order.id_message_cart[-1])
        self.generate_and_send_start_kb(order.user, Text.get_body(Text.CHANGE_COUNT))

    def send_line_product_cart(self, order: Order, line_product,  num_line: int, message_id=None):
        txt = f'\t{num_line}. {line_product.product.title} ({line_product.count} {Text.get_body(Text.PCS)}.): ' \
              f'\t{line_product.sum} {Text.get_body(Text.CURRENCY)}.\n'
        kb_product = self.generate_kb_product_cart(order, num_line - 1)
        result = message_id
        try:
            if message_id:
                self.edit_message_text(txt, order.user.user_id, message_id, reply_markup=kb_product)
            else:
                result = self.send_message(order.user.user_id, txt, reply_markup=kb_product)
        except  ApiException:
            pass

        return result

    def send_footer_cart(self, order: Order, message_id=None):
        kb = InlineKeyboardMarkup()
        button = []
        button.append(InlineKeyboardButton(text=Text.get_body(Text.ORDER_PROCESSED),
                                           callback_data=f'{HENDLER_ORDER}{SEPARATOR}{order.id}{SEPARATOR}{Order.ORDER_PROCESSED}'))
        button.append(InlineKeyboardButton(text=Text.get_body(Text.ORDER_CANCELED),
                                           callback_data=f'{HENDLER_ORDER}{SEPARATOR}{order.id}{SEPARATOR}{Order.ORDER_CANCELED}'))
        kb.add(*button)
        txt = f'{Text.get_body(Text.ORDER_STATUS)}: {order.get_text_status_order()}\n'
        txt += f'\n{Text.get_body(Text.SUMM_TO_PAY)}: {order.sum} {Text.get_body(Text.CURRENCY)}.'
        result = message_id
        try:
            if message_id:
                self.edit_message_text(txt, order.user.user_id, message_id, reply_markup=kb)
            else:
                result = self.send_message(order.user.user_id, txt, reply_markup=kb)
        except  ApiException:
            pass

        return result

    def send_cart(self, message: str):
        user = User.get_user(chat=message.chat)
        order = Order.get_active_order(user)

        order.last_request = None
        order.id_message_cart = []

        # 1 Шапка корзины
        txt = f'{Text.get_body(Text.ORDER)} №{order.nom} {Text.get_body(Text.FROM)} {order.date:%d.%m.%Y %H:%M}.\n'
        result = self.send_message(order.user.user_id, txt)
        order.id_message_cart.append(result.message_id)

        # 2 Товары
        nom = 0
        for item in order.products:
            nom += 1
            result = self.send_line_product_cart(order, item, nom)
            order.id_message_cart.append(result.message_id)

        # 3 Подвал корзины
        # kb = InlineKeyboardMarkup()
        # button = []
        # button.append(InlineKeyboardButton(text=Text.get_body(Text.ORDER_PROCESSED),
        #                     callback_data=f'{HENDLER_ORDER}{SEPARATOR}{order.id}{SEPARATOR}{Order.ORDER_PROCESSED}'))
        # button.append(InlineKeyboardButton(text=Text.get_body(Text.ORDER_CANCELED),
        #                     callback_data=f'{HENDLER_ORDER}{SEPARATOR}{order.id}{SEPARATOR}{Order.ORDER_CANCELED}'))
        # kb.add(*button)
        # txt = f'{Text.get_body(Text.ORDER_STATUS)}: {order.get_text_status_order()}\n'
        # txt += f'\n{Text.get_body(Text.SUMM_TO_PAY)}: {order.sum} {Text.get_body(Text.CURRENCY)}.'
        #
        # result = self.send_message(order.user.user_id, txt, reply_markup=kb)
        result = self.send_footer_cart(order)
        order.id_message_cart.append(result.message_id)

        order.save()

    def send_order(self, order: Order, reply_markup=None, message_id=None):
        if not order:
            return

        txt = f'{Text.get_body(Text.ORDER)} №{order.nom} {Text.get_body(Text.FROM)} {order.date:%d.%m.%Y %H:%M}.\n'
        all_sum = 0
        for item in order.products:
            all_sum += item.sum
            txt += f'\t{item.product.title} ({item.count} {Text.get_body(Text.PCS)}.): ' \
                   f'\t{item.sum} {Text.get_body(Text.CURRENCY)}.\n'

        txt += f'\n{Text.get_body(Text.ORDER_STATUS)}: {order.get_text_status_order()}\n'

        txt += f'\n{Text.get_body(Text.SUMM_TO_PAY)}: {all_sum} {Text.get_body(Text.CURRENCY)}.'

        if message_id:
            self.edit_message_text(txt, order.user.user_id, message_id, reply_markup=reply_markup)
        else:
            self.send_message(order.user.user_id, txt, reply_markup=reply_markup)

    def next_status_order(self, order: Order, order_status):
        order.status = order_status
        order.save()

        text = order.get_text_status_order()
        self.delete_message_from_cart(order)
        self.send_order(order)

        self.generate_and_send_start_kb(order.user, text)

    def send_short_order(self, order):
        kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text=Text.get_body(Text.SHOW_ORDER),
                                      callback_data=f'{HENDLER_HISTORY_ORDER}{SEPARATOR}{order.id}')
        kb.add(button)

        txt = f'{Text.get_body(Text.ORDER)} №{order.nom} {Text.get_body(Text.FROM)} {order.date:%d.%m.%Y %H:%M}.\n'
        txt += f'{Text.get_body(Text.ORDER_STATUS)}: {order.get_text_status_order()}\n'
        txt += f'{Text.get_body(Text.SUMM_TO_PAY)}: {order.sum} {Text.get_body(Text.CURRENCY)}.'
        self.send_message(order.user.user_id, txt, reply_markup=kb)

    def get_history_orders(self, user):
        orders = Order.objects(user=user).order_by('date')
        for order in orders:
            self.send_short_order(order)

    def process_order(self, order: Order, message_id=None):
        #  Якщо нема телефона чи фіо то перепитати
        user = order.user

        if not order.telephone_recipients:
            self.send_message_input_field_user(user, order, order.REQUEST_TELEPHONE, Text.get_body(Text.ENTER_PHONE_NUMBER),
                                              user.telephone, message_id )
            return

        if not order.name_recipients:
            self.send_message_input_field_user(user, order, order.REQUEST_NAME, Text.get_body(Text.ENTER_LAST_FIST_NAME),
                                                  user.name, message_id)
            return

        self.next_status_order(order, Order.ORDER_PROCESSED)

    def send_message_input_field_user(self, user: User, order: Order, status, text: str, value: str,  message_id=None):
        if value and len(value)>2:
            kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            kb.add(KeyboardButton(value))
        else:
            kb = ReplyKeyboardRemove()

        order.last_request = status
        order.save()

        # if message_id:
        #     self.delete_message(user.user_id, message_id)
        self.send_message(user.user_id, text, reply_markup=kb)

    def set_telephone_user(self, user: User, text: str):
        order = Order.get_active_order(user)

        order.telephone_recipients = text
        order.last_request = None
        user.telephone = text

        try:
            order.save()
            user.save()
        except ValidationError:
            order.reload()
            user.reload()
            text = f'{Text.get_body(Text.INCORRECT_PHONE_NUMBER)}\n{Text.get_body(Text.RE_ENTER)}'
            self.send_message_input_field_user(user, order, order.REQUEST_TELEPHONE, text,
                                                  user.telephone)
            return
        self.process_order(order)

    def set_name_user(self, user: User, text: str):
        order = Order.get_active_order(user)

        if len(text) <= 2:
            text = f'{Text.get_body(Text.INCORRECN_NAME)}\n{Text.get_body(Text.RE_ENTER)}'
            self.send_message_input_field_user(user, order, order.REQUEST_NAME, text,
                                                  user.name)
            return

        order.name_recipients = text
        order.last_request = None
        order.save()

        user.name = text
        user.save()

        self.process_order(order)








