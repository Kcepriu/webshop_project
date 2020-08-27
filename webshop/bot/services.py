from typing import List, Union
from telebot import TeleBot
from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           KeyboardButton)

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
            title_ = category.title if category else  Text.get_body(Text.RETURN_TO_TOP)

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
            button = InlineKeyboardButton(text = Text.get_body(Text.ADD_TO_CART),
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

        #Якщо є раніше створені закази, то додамо кнопку для виклику історії заказів
        count_orders = Order.get_count_orders(user)
        if count_orders:
            buttons.append(KeyboardButton(f'{Text.get_body(Text.ORDER_HISTORY)} ({count_orders})'))

        kb.add(*buttons)
        return kb

    def generate_and_send_start_kb(self, user: User,  chat_id: int, text: str):
        kb = self.generate_start_kb(user)
        self.send_message(chat_id, text, reply_markup=kb)

    def generate_and_edit_start_kb(self, user: User,  chat_id: int, message_id: int, text: str):
        kb = self.generate_start_kb(user)
        self.edit_message_text(text, chat_id, message_id=message_id, inline_message_id=message_id, reply_markup=kb)

    def send_cart(self, message: str):
        user = User.get_user(chat=message.chat)
        order = Order.get_active_order(user)

        kb = InlineKeyboardMarkup()
        button = []
        button.append(InlineKeyboardButton(text=Text.get_body(Text.ORDER_PROCESSED),
            callback_data=f'{HENDLER_ORDER}{SEPARATOR}{order.id}{SEPARATOR}{Order.ORDER_PROCESSED}'))
        button.append(InlineKeyboardButton(text=Text.get_body(Text.ORDER_CANCELED),
            callback_data=f'{HENDLER_ORDER}{SEPARATOR}{order.id}{SEPARATOR}{Order.ORDER_CANCELED}'))
        kb.add(*button)
        self.send_order(message.chat.id, order, reply_markup=kb)

    def send_order(self,  chat_id: int, order: Order, reply_markup=None, message_id=None):
        if not order:
            return

        txt = f'{Text.get_body(Text.ORDER)} №{order.nom} {Text.get_body(Text.FROM)} {order.date:%d.%m.%Y %H:%M}.\n'
        all_sum = 0
        for item in order.products:
            all_sum += item.summ
            txt += f'\t{item.product.title} ({item.count} {Text.get_body(Text.PCS)}.): ' \
                   f'\t{item.summ} {Text.get_body(Text.CURRENCY)}.\n'

        txt += f'\n{Text.get_body(Text.ORDER_STATUS)}: {order.get_text_status_order()}\n'

        txt += f'\n{Text.get_body(Text.SUMM_TO_PAY)}: {all_sum} {Text.get_body(Text.CURRENCY)}.'


        if message_id:
            self.edit_message_text(txt, chat_id, message_id, reply_markup=reply_markup)
        else:
            self.send_message(chat_id, txt, reply_markup=reply_markup)

    def next_status_order(self, message: str, order_id: str, order_status):
        user = User.get_user(chat=message.chat)
        order = Order.objects.get(id=order_id)
        order.status = order_status
        order.save()

        text = order.get_text_status_order()

        self.send_order(message.chat.id, order, message_id=message.message_id)
        self.generate_and_send_start_kb(user, message.chat.id, text)

    def send_short_order(self, order):
        pass

    def get_history_orders(self, user):
        orders = Order.objects(user=user).order_by('-date')
        for order in orders:
            pass







