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

app = Flask(__name__)

line_bot_api = LineBotApi('9vW9RRY+UoIEWpuV577G6fRs4X8RHe9tMzZEXd2i40epSOFxDq8v2P5ITT3uVV4juN6SkXktJ+ToP8PLtDSjIwZ0Mu4TD1K7chjvEjMxIfKdVCR6tayxbmg1do1Oz1+POVbOOfBGG10J7nSJJeKfdgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('dbc1bb75c6af4728628446ef6ef88b38')


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

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(port=3000)