from flask import Blueprint
from .config import WEBHOOK_PRIFIX
from .hendlers import bot_instance

from flask import request, abort
from telebot.types import Update


bot_app = Blueprint('bot', __name__)

@bot_app.route(WEBHOOK_PRIFIX, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot_instance.process_new_updates([update])
        return ''
    else:
        abort(403)