from typing import List, Union
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..db import Category, Product, New
from .lookups import SEPARATOR
from .config import NO_PHOTO_URL


class WebShopBot(TeleBot):
    def generety_categories_kb(self, categories: List[Union[Category, None]], **kwargs):
        kb = InlineKeyboardMarkup(**kwargs)
        buttons = []
        for category in categories:
            id_ = category.id if category else None
            title_ = category.title if category else 'Вернуться на верхний уровеь'

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
            button = InlineKeyboardButton(text = 'Добавить в корзину',
                                          callback_data=f'{Product.__name__}{SEPARATOR}{product.id}')
            kb.add(button)
            self.send_photo(chat_id, product.url_photo if product.url_photo else NO_PHOTO_URL,
                            product.description, reply_markup=kb)

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





