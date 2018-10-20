import json
from urllib.request import urlopen, Request
import city_id_list

# 例外処理を定義する
class OverLengthError(Exception):
    """Error for input data length

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class EmptyError(Exception):
    """Error which input data is empty.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self,  expression, message):
        self.expression = expression
        self.message = message

"""
    例「天気 地名」という形式の投稿に対して、livedoor天気情報のリストを検索し、
    ヒットした場合、その地名の天気予報を返す

    Attributes:
    text -- post messages of slack user
"""
def getWeather(text):
    # Weather Hacksのリクエストパラメータ
    weather_api_url = 'http://weather.livedoor.com/forecast/webservice/json/v1'

    # slackへの返答を初期化
    response_string = ''

    # URLパラメータであるcity_idを初期化
    city_id = ''

    # slackの入力を分割し、地名をdiv_text[1]に格納
    div_text = text.split()

    # 入力文字数の上限を設定
    PLACE_LENGTH_LIMIT = 5
    print(div_text)

    try:
        # 入力文字列が空でないことを確認
        if len(div_text) < 1:
            raise EmptyError(text,"InputCheckError")

        place = div_text[2] # 地名
        print(place)
        place_length = len(place) # 地名の長さを測定

        # 地名が文字列であるかをチェック
        if isinstance(place, str) == False:
            raise TypeError(place,"InputCheckError")

        # 入力文字数のチェック
        if place_length > PLACE_LENGTH_LIMIT:
            raise OverLengthError(place,"InputCheckError")

        # 定義した関数. city_idのエンドポイントである"http://weather.livedoor.com/forecast/rss/primary_area.xml"から
        # 地名一覧を取ってくる。
        city_dict = city_id_list.get_weather_list()
        print(city_dict)

        # 地名でリストを検索し、ヒットした地名のcity_idを格納
        # 地名が city_dict から発見できない場合、KeyErrorが発生して、expect文へ
        city_id = city_dict[place]
        print(city_id)

        # livedoor天気情報のWeather HacksのURLを生成
        url = weather_api_url + "?city=" + city_id

        # URLから天気情報をJSON形式で取得し、response_dictへ格納
        http_response = Request(url) # レスポンスを出す
        http_response = urlopen(http_response)
        response_dict = json.loads(http_response.read())

        # 都道府県名を取得
        title = response_dict["title"]

        # 天気概況文を取得
        description = response_dict["description"]["text"]

        # 地名をレスポンスに追加
        response_string += title + "です。:nerd_face:\n\n"

        # JSONから，今日・明日・明後日の天気を取得し，配列に格納
        forecasts_array = response_dict["forecasts"]

        forcast_array = []

        for forcast in forecasts_array:
            telop = forcast["telop"] # 天気情報を取得
            telop_icon = ''

            if telop.find('雪') > -1:
                telop_icon = ':showman:'

            elif telop.find('雷') > -1:
                telop_icon = ':thunder_cloud_and_rain:'

            elif telop.find('雨') > -1:
                telop_icon = ':umbrella:'

            elif telop.find('曇') > -1:
                telop_icon = ':cloud:'

            elif telop.find('晴') > -1:
                if telop.find('曇') > -1:
                    telop_icon = ':partly_sunny:'
                elif telop.find('雨') > -1:
                    telop_icon = ':partly_sunny_rain:'
                else:
                    telop_icon = ':sunny:'


            # 気温の記述を生成
            temperature = forcast["temperature"]
            min_temp = temperature["min"]
            max_temp = temperature["max"]
            output_temp = ''

            # min_temp,max_tempが存在していれば
            if min_temp is not None:
                if len(min_temp) > 0:
                    output_temp += '\n最低気温は' + min_temp["celsius"] + "度です。"
            if max_temp is not None:
                if len(max_temp) > 0:
                    output_temp += '\n最高気温は' + max_temp["celsius"] + "度です。"

            forcast_array.append(forcast["dateLabel"] + ' ' + telop + telop_icon + output_temp)

        if len(forcast_array) > 0:
            response_string += '\n\n'.join(forcast_array)

        response_string += '\n\n' + description

    # 例外処理
    except TypeError as e:
        response_string = "地名は文字列で入力してくださいね。"
        print(e)
        print("Input Data Type is not characters. Please try again.")

    except EmptyError as e:
        response_string = "地名の指定がされていませんよ...「天気 地名」で再度入力してください．"
        print(e)
        print("Input Data is Empty. Please try again.")

    except OverLengthError as e:
        response_string = "地名は5文字以内の日本語で入力してね。"
        print(e)
        print("Over 5 characters. Please try again.")

    except KeyError as e:
        response_string = "ごめんね。その地名はサポートしてないんだ。"
        print(e)
        print("Your Input couldn't discover. Please try another word again.")

    except Exception as e:
        response_string = "変なバグがでちった。めんご。"
        print(e)
        print("Unknown error.")

    return response_string


def getWeatherPlace():
    # 定義した関数. city_idのエンドポイントである"http://weather.livedoor.com/forecast/rss/primary_area.xml"から
    # 地名一覧を取ってくる。
    city_dict = city_id_list.get_weather_list()
    city_place_list = '\n'.join(city_dict.keys())
    return city_place_list
