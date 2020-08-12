from typing import List

from ..db.models import Category

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
class WebShopBot(TeleBot):
    def generety_categories_kb(self, categories: List[Category], **kwargs):
        kb = InlineKeyboardMarkup(**kwargs)
        buttons = InlineKeyboardButton(

        )
