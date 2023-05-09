import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# ======python的函數庫==========
import requests
import tempfile
import os
import datetime
import openai
import time
from bs4 import BeautifulSoup
# ======python的函數庫==========
import configparser
app = Flask(__name__)

""" config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
 """

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    """ line_bot_api.reply_message(event.reply_token, TextSendMessage(msg)) """
    if msg.find('查詢未完成工單') != -1:
        url = 'https://sys.leadyoung.com.tw/assets/Home/LINE_BOT_TEST?ID='+msg
        # 發送GET請求
        response = requests.get(url)
        # 解析HTML內容
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(5)
    elif msg.find('ASK GPT') != -1:
        GPT_answer = GPT_response(msg)
        print(GPT_answer)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(GPT_answer))


def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(
        model="text-davinci-003", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。', '')
    return answer


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
