import requests
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
    message=text=event.message.text
    url="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=rdec-key-123-45678-011121314"
    data=requests.get(url)
    data_json = data.json()    # 轉換成 JSON 格式

    placesqty=len(data_json['records']['location'])
    weatherqty=len(data_json['records']['location'][0]['weatherElement'])
    weathertime=len(data_json['records']['location'][0]['weatherElement'][0]['time'])

    def datainfo(search):
        for i in range(placesqty):
            if message==data_json['records']['location'][i]['locationName']:
                print(data_json['records']['location'][i]['locationName'])       
                for j in range(weathertime):
                    print(data_json['records']['location'][i]['weatherElement'][0]['time'][j]['startTime']+"-"+data_json['records']['location'][i]['weatherElement'][0]['time'][j]['endTime'])
                    print(data_json['records']['location'][i]['weatherElement'][0]['time'][j]['parameter']['parameterName'])
                    print("降雨機率:"+data_json['records']['location'][i]['weatherElement'][1]['time'][j]['parameter']['parameterName']+"%")
                    print(data_json['records']['location'][i]['weatherElement'][2]['time'][j]['parameter']['parameterName']+"度-"+data_json['records']['location'][i]['weatherElement'][4]['time'][j]['parameter']['parameterName']+"度")
                    print(data_json['records']['location'][i]['weatherElement'][3]['time'][j]['parameter']['parameterName'])
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))



if __name__ == "__main__":
    app.run()