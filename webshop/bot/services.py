from typing import List, Union
from telebot import TeleBot
from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           KeyboardButton)
from mongoengine.errors import ValidationError

from ..db import Category, Product, New, Text, Order, User
from .lookups import SEPARATOR, HENDLER_ORDER, HENDLER_CATEGORY, HENDLER_PRODUCT, HENDLER_HISTORY_ORDER
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
        self.send_message(user.user_id, text, reply_markup=kb)

    def send_cart(self, message: str):
        user = User.get_user(chat=message.chat)
        order = Order.get_active_order(user)

        user.las_request = None
        user.save()

        kb = InlineKeyboardMarkup()
        button = []
        button.append(InlineKeyboardButton(text=Text.get_body(Text.ORDER_PROCESSED),
                                           callback_data=f'{HENDLER_ORDER}{SEPARATOR}{order.id}{SEPARATOR}{Order.ORDER_PROCESSED}'))
        button.append(InlineKeyboardButton(text=Text.get_body(Text.ORDER_CANCELED),
                                           callback_data=f'{HENDLER_ORDER}{SEPARATOR}{order.id}{SEPARATOR}{Order.ORDER_CANCELED}'))
        kb.add(*button)
        self.send_order(order, reply_markup=kb)

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

    # def next_status_order(self, message: str, order_id: str, order_status):
    def next_status_order(self, order: Order, message_id: str, order_status):
        # order.status = order_status
        order.save()

        text = order.get_text_status_order()

        self.send_order(order, message_id=message_id)
        self.generate_and_send_start_kb(order.user, text)

    def send_short_order(self, order):
        kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text=Text.get_body(Text.SHOW_ORDER),
                                      callback_data=f'{HENDLER_HISTORY_ORDER}{SEPARATOR}{order.id}')
        kb.add(button)

        all_sum = 10

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

        # if self.send_message_input_telephone_user(user, 'Введите номер телефона', message_id):
        if self.send_message_input_field_user(user, User.REQUEST_TELEPHONE, 'Введите номер телефона',
                                              lambda user: user.telephone, message_id ):
            return

        # if self.send_message_inpun_name_user(user, 'Введите ФИО', message_id):
        if self.send_message_input_field_user(user, User.REQUEST_NAME, 'Введите ФИО',
                                                  lambda user: (user.last_name or user.first_name), message_id):
            return

        # bot_instance.next_status_order(call.message, call.data.split(SEPARATOR)[1], Order.ORDER_PROCESSED)

    def send_message_input_telephone_user(self, user: User, text: str, message_id=None):
        if user.telephone:
            return

        user.las_request = User.REQUEST_TELEPHONE
        user.save()

        if message_id:
            self.edit_message_text(text, user.user_id, message_id)
        else:
            self.send_message(user.user_id, text)
        return True

    def set_telephone_user(self, user: User, text: str):
        user.telephone = text
        try:
            user.save()
        except ValidationError:
            user.reload()
            text = f'Ввели не коретный номер телефона\nПовторите ввод'
            # self.send_message_input_telephone_user(user, text)
            self.send_message_input_field_user(user, User.REQUEST_TELEPHONE, text,
                                                  lambda user: user.telephone)
            return

        order = Order.get_active_order(user)
        self.process_order(order)


    def send_message_inpun_name_user(self, user: User, text: str, message_id=None):
        if user.last_name or user.first_name:
            return

        user.las_request = User.REQUEST_NAME
        user.save()

        if message_id:
            self.edit_message_text(text, user.user_id, message_id)
        else:
            self.send_message(user.user_id, text)
        return True


    def send_message_input_field_user(self, user: User, status, text: str, funct,  message_id=None):
        if funct(user):
            return

        user.las_request = status
        user.save()

        if message_id:
            self.edit_message_text(text, user.user_id, message_id)
        else:
            self.send_message(user.user_id, text)
        return True



