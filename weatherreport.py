import os
import json
import datetime


import requests


my_key = "15c0f696cc7d41dda7c982f76e86c6d6"
# 从测试号信息获取
appID = "wx0c4b980e5b3906ad"
appSecret = "79c6495c6650756c586087710019b81a"
# 收信人ID即 用户列表中的微信号，见上文
openId = {
    "myself": "ol5Kd6F02-rK19fhWJhSkLOCt-HE",
    "test_acc": "ol5Kd6DAVz0_w7awSB1K4h1MW6CE",
}
# 天气预报模板ID
weather_template_id = "noZ2_QYEdbL37_WNawaoitPKW230WEpfiaRbM2_RHI4"


def get_access_token():
    # 获取access token的url
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appID.strip()}&secret={appSecret.strip()}"
    response = requests.get(url).json()
    print(response)
    access_token = response.get("access_token")
    return access_token


def get_location(city):
    loc_url = f"https://geoapi.qweather.com/v2/city/lookup?location={city}&key={my_key}"
    res_dict = requests.get(loc_url).json()

    locationID = res_dict["location"][0]["id"]
    return locationID


def get_weather(city):
    locationID = get_location(city)
    paragrams = {"key": my_key, "location": locationID}
    urls = "https://devapi.qweather.com/v7/weather/now?"
    response = requests.get(url=urls, params=paragrams).json()

    weather_res = response["now"]
    weather_infodict = {
        "city": city,
        "temp": weather_res["temp"],
        # "feelsLike": weather_res["feelsLike"],
        "weather_text": weather_res["text"],
        "wind_direction": weather_res["windDir"],
        # "wind_scale": weather_res["windScale"],
        # "wind_speed": weather_res["windSpeed"],
        # "humidity": weather_res["humidity"],
    }
    return weather_infodict


def send_weather(access_token, weather):
    # touser 就是 openID
    # template_id 就是模板ID
    # url 就是点击模板跳转的url
    # data就按这种格式写，time和text就是之前{{time.DATA}}中的那个time，value就是你要替换DATA的值

    import datetime

    today = datetime.date.today()
    today_str = today.strftime("%Y年%m月%d日")

    body = {
        "touser": openId["myself"].strip(),
        "template_id": weather_template_id.strip(),
        "url": "https://weixin.qq.com",
        "data": {
            "date": {"value": today_str},
            "region": {"value": weather["city"]},
            "weather": {"value": weather["weather_text"]},
            "temp": {"value": weather["temp"] + "摄氏度"},
            "wind_dir": {"value": weather["wind_direction"]},
            "today_note": {"value": "早上好"},
        },
    }
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    print(requests.post(url, json.dumps(body)).text)


def weather_report(city):
    # 1.获取access_token
    access_token = get_access_token()
    # 2. 获取天气
    weather = get_weather(city)
    print(f"天气信息： {weather}")
    # 3. 发送消息
    send_weather(access_token, weather)


if __name__ == "__main__":
    weather_report("乐陵")
