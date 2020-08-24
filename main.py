import time

from webshop.bot import bot_instance
from flask import Flask, abort
from webshop.bot.config import WEBHOOK_PRIFIX, WEBHOOK_URL
from flask import request
from telebot.types import Update

app = Flask(__name__)
@app.route(WEBHOOK_PRIFIX, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot_instance.process_new_updates([update])
        return ''
    else:
        abort(403)





if __name__ == '__main__':
    bot_instance.remove_webhook()
    time.sleep(1)

    bot_instance.polling()
    # bot_instance.infinity_polling()

    # bot_instance.set_webhook(
    #     url=WEBHOOK_URL,
    #     certificate=open('webhook_cert.pem', 'r')
    # )
    # app.run(debug=True)