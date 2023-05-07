from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from Controller import Controller

import os

import requests

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_API_KEY'))
handler = WebhookHandler(os.getenv('HANDLER_URL'))

GOOGLE_MACRO_WEBHOOK = os.getenv('GOOGLE_MACRO_WEBHOOK')
WEBHOOK_SITE = os.getenv('WEBHOOK_SITE')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    data_list = request.get_json()

    headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': request.headers['X-Line-Signature']
    }

    requests.post(GOOGLE_MACRO_WEBHOOK, headers=headers, data=request.get_data())
    requests.post(WEBHOOK_SITE, headers=headers, data=request.get_data())

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=c.sendMessage(event.message.text)))
    except ValueError:
        pass

if __name__ == "__main__":
    c = Controller()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
