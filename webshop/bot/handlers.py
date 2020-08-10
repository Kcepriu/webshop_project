# тут пишу на заняттях. Мій можудь miamn
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from .config import TOKEN
from telebot import TeleBot
from ..db.models import Text

from .keyboards import START_KB

bot = TeleBot(TOKEN)
@bot.message_handler(command=['start'])
def start(messsage):
    txt = Text.objects.get(title=Text.GRITINGS).body
    bot.send_message(
        messsage.chat.id,
        txt, reply_markup=
    )