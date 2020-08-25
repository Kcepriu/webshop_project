from typing import List, Union
from telebot import TeleBot
from telebot.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           KeyboardButton)

from ..db import Category, Product, New, Text
from .lookups import SEPARATOR
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
                callback_data=f'{Category.__name__}{SEPARATOR}{id_}'))

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
                                          callback_data=f'{Product.__name__}{SEPARATOR}{product.id}')
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

    def update_keyboard_markup(self, user, chat_id, txt):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [KeyboardButton(button) for button in START_KB.values()]

        count_products_from_cart = user.get_count_products_active_order()
        # хотів причепити кількість товарів в корзині, але не зрозуміло як відслідковувати натискання кнопки
        if count_products_from_cart:
            buttons.append(KeyboardButton(Text.get_body(Text.GO_TO_CART)) )

        count_orders = user.get_count_orders()
        if count_orders:
            buttons.append(KeyboardButton(Text.get_body(Text.ORDER_HYSTORY)))

        kb.add(*buttons)
        self.send_message(chat_id, txt, reply_markup=kb)





