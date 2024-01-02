import requests
import json
from config import condition, win_dir

def request():
    r = requests.get("https://api.weather.yandex.ru/v2/informers", 
                    headers={"X-Yandex-API-Key": "c617ce91-d2d4-459c-ac1b-1bb9c719967a"},
                    params={"lat": "48.7194", "lon": "44.5018", "lang": "ru_RU"})
    d = json.loads(r.text)

    temp = d["fact"]["temp"]
    feels_like = d["fact"]["feels_like"]
    con = d["fact"]["condition"]
    wind_speed = d["fact"]["wind_speed"]
    wind_dir = d["fact"]["wind_dir"]

    con = condition[con]
    wind_dir = win_dir[wind_dir]

    s = f"Сейчас на улице {temp}.\nОщущается как {feels_like}.\nВ городе сейчас {con}.\nСкорость ветра равна {wind_speed} метра в секунду.\nНаправление ветра {wind_dir}."
    
    return s
