import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from selenium import webdriver

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
from requests_html import HTMLSession
app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


""" static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET')) """


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
    line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))
    # 创建一个 HTMLSession 实例
    url = 'https://sys.leadyoung.com.tw/assets/Home/LINE_BOT_TEST?ID=2023/05/08'

    # 發送GET請求
    response = requests.get(url)

    # 解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')
    time.sleep(5000)
    # 找到所有的超連結
    links = soup.find_all(
        'div', class_="dd", limit=1)

    # 輸出每個超連結的文字和URL
    for link in links:
        print(link.text)


# 等待 JS 加载完成
""" response.html.render() """
""" driver = webdriver.Chrome('./chromedriver.exe')
    driver.get(
        'https://sys.leadyoung.com.tw/assets/Home/LINE_BOT_TEST?ID='+msg)
    time.sleep(10) """


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
