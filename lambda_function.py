import json
import os
import livedoor_tenki
import logging
from urllib.request import urlopen, Request
from urllib.parse import parse_qs

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# lambda function
def lambda_handler(event, content):
    #受け取った情報をCloud Watchログに出力
    logging.info(json.dumps(event, indent=4))
    print(event)
    token = os.environ.get("SLACK_TOKEN")

    bot_name = 'slack_tenki'

    # slackからの投稿を slack_input_text へ格納
    slack_input_text = str(event["event"]["text"])
    print(slack_input_text)

    tenki = slack_input_text.find('天気')
    basho = slack_input_text.find('場所一覧')

    if basho != -1:
        print("場所検索")
        msg = livedoor_tenki.getWeatherPlace()

    # slackの投稿に「天気」の文字列が入っている場合、livedoor天気情報
    if tenki != -1:
        print("天気表示")
        msg = livedoor_tenki.getWeather(slack_input_text)


     # Slackにメッセージを投稿する
    post_message_to_slack_channel(msg, event["event"]["channel"])

    response = {
        'statusCode': 200,
    }

    return response

def post_message_to_slack_channel(message: str, channel: str):
    # Slackのchat.postMessage APIを利用して投稿する
    # ヘッダーにはコンテンツタイプとボット認証トークンを付与する
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer {0}".format(os.environ["SLACK_BOT_USER_ACCESS_TOKEN"])
    }
    data = {
        "token": os.environ["SLACK_APP_AUTH_TOKEN"],
        "channel": channel,
        "text": message
    }
    req = Request(url, data=json.dumps(data).encode("utf-8"), method="POST", headers=headers)
    urlopen(req)
    return
