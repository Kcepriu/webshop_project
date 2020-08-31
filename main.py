import time

from webshop.bot import bot_instance
from flask import Flask

# from webshop.bot.config import WEBHOOK_PRIFIX, WEBHOOK_URL
# from flask import request, abort
# from telebot.types import Update

from webshop.bot.config import WEBHOOK_URL
from webshop.api import api_app
from webshop.bot import bot_app

app = Flask(__name__)
app.register_blueprint(api_app)
app.register_blueprint(bot_app)

# @app.route(WEBHOOK_PRIFIX, methods=['POST'])
# def webhook():
#     if request.headers.get('content-type') == 'application/json':
#         json_string = request.get_data().decode('utf-8')
#         update = Update.de_json(json_string)
#         bot_instance.process_new_updates([update])
#         return ''
#     else:
#         abort(403)





if __name__ == '__main__':
    bot_instance.remove_webhook()
    time.sleep(2)

    # bot_instance.polling()

    # bot_instance.infinity_polling()

    bot_instance.set_webhook(
        url=WEBHOOK_URL,
        certificate=open('webhook_cert.pem', 'r')
    )
    app.run(debug=True)
