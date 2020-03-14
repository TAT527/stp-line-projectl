# -*- coding: utf-8 -*-
import os
import sys
from account_response import Response
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
# インスタンス生成
res = Response()

# Herokuの変数からトークンなどを取得
channel_secret = os.environ['LINE_CHANNEL_SECRET']
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# LINEからのWebhook
@app.route("/callback", methods = ['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合
# reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
# 第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    #入力された内容(event.message.text)に応じて返信する
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text = os.environ[res.getResponse(event.message.text)])
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))