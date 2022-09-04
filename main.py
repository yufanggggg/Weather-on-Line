import requests
import json
import pandas as pd 
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

url="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=rdec-key-123-45678-011121314"
data=requests.get(url)
data_json = data.json()    # 轉換成 JSON 格式

placesqty=len(data_json['records']['location'])
weatherqty=len(data_json['records']['location'][0]['weatherElement'])
weathertime=len(data_json['records']['location'][0]['weatherElement'][0]['time'])

def datainfo(search):
    for i in range(placesqty):
        if search==data_json['records']['location'][i]['locationName']:
            print(data_json['records']['location'][i]['locationName'])       
            for j in range(weathertime):
                print(data_json['records']['location'][i]['weatherElement'][0]['time'][j]['startTime']+"-"+data_json['records']['location'][i]['weatherElement'][0]['time'][j]['endTime'])
                print(data_json['records']['location'][i]['weatherElement'][0]['time'][j]['parameter']['parameterName'])
                print("降雨機率:"+data_json['records']['location'][i]['weatherElement'][1]['time'][j]['parameter']['parameterName']+"%")
                print(data_json['records']['location'][i]['weatherElement'][2]['time'][j]['parameter']['parameterName']+"度-"+data_json['records']['location'][i]['weatherElement'][4]['time'][j]['parameter']['parameterName']+"度")
                print(data_json['records']['location'][i]['weatherElement'][3]['time'][j]['parameter']['parameterName'])

access_token = 'oOxJjPf56femjnkQ2KPp6RPj0YXVuOb5Ru2Wkd0GviuiHkyGY3TtcyEsw5rPnGpvuN6SkXktJ+ToP8PLtDSjIwZ0Mu4TD1K7chjvEjMxIfI+7GVp2TI54H3K44QUlHQs1dL6YKelBqqjrSR4S5ggowdB04t89/1O/w1cDnyilFU='
secret = '8fc22a04a28183b7fd645c46fe866959'
line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
handler = WebhookHandler(secret)                     # 確認 secret 是否正確
def callback():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        line_bot_api.reply_message(tk,TextSendMessage(msg))  # 回傳訊息
        print(msg, tk)                                       # 印出內容
    except:
        print(body) 
    return 'OK'
