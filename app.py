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

app = Flask(__name__)

line_bot_api = LineBotApi('9EXM/EXlA0Ny45voTbbXBHwcGQrqdrhGUrnWu0HCziIRfBMXrD6zqa0e2ZL8VcYyeMq5USfq+bCAFwsUpLunzyoWZ1XNvCRuX70Urj5+zunWkt/dOU1i9P/uL533UAfN+zZTbzc2ddhnVdzrdbG+SAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9358a9068fd4abd2131b522197e8ca56')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True, parse_form_data=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
##### 基本上程式編輯都在這個function #####

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    url="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=rdec-key-123-45678-011121314"
    data=requests.get(url)
    data_json = data.json()    # 轉換成 JSON 格式
    placesqty=len(data_json['records']['location'])
    weatherqty=len(data_json['records']['location'][0]['weatherElement'])
    weathertime=len(data_json['records']['location'][0]['weatherElement'][0]['time'])
    result=[]
    for i in range(placesqty):
            fresult=result.append(data_json['records']['location'][i]['locationName'])
    print(message)
    content=[]
    for i in range(placesqty):
        if message==result[i]:   
            for j in range(weathertime):
                fcontent=content.append(data_json['records']['location'][i]['weatherElement'][0]['time'][j]['startTime']+"-"+data_json['records']['location'][i]['weatherElement'][0]['time'][j]['endTime']+"\n"+data_json['records']['location'][i]['weatherElement'][0]['time'][j]['parameter']['parameterName']+"，"+data_json['records']['location'][i]['weatherElement'][3]['time'][j]['parameter']['parameterName']+"\n"+"氣溫:"+data_json['records']['location'][i]['weatherElement'][2]['time'][j]['parameter']['parameterName']+"度-"+data_json['records']['location'][i]['weatherElement'][4]['time'][j]['parameter']['parameterName']+"度，"+"降雨機率:"+data_json['records']['location'][i]['weatherElement'][1]['time'][j]['parameter']['parameterName']+"%")
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='\n\n'.join(content)))

if __name__ == "__main__":
    app.run()
