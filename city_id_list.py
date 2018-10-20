from xml.etree import ElementTree
from urllib.request import urlopen, Request, urlretrieve

def get_weather_list():
    # 主要都市とidの対応関係が記載されたURL。今回はこの中身をコピって　primary_areaに配置した。
    # "http://weather.livedoor.com/forecast/rss/primary_area.xml"

    # parse()関数でファイルを読み込んでElementTreeオブジェクトを得る。
    tree = ElementTree.parse('primary_area.xml')

    # getroot()メソッドでXMLのルート要素（この例ではrss要素）に対応するElementオブジェクトを得る
    root = tree.getroot()

    # 都市リスト:city_dictの初期化
    city_dict = {}

    # findall()メソッドでXPathにマッチする要素のリストを取得する
    for pref in root.findall('.//pref'):

        pref_name = pref.get('title')

        for city in pref.findall('.//city'):
            city_name = city.get('title')
            city_id = city.get('id')
            city_dict[city_name] = city_id

    return city_dict
