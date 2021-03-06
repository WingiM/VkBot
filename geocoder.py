import os
import requests
from dotenv import load_dotenv

load_dotenv('.env')

STATIC_API_URL = "https://static-maps.yandex.ru/1.x/?"
GEOCODER_API_URL = f"https://geocode-maps.yandex.ru/1.x/?"


def search(toponym, maptype):
    params = {
        "apikey": os.getenv("GEOCODER_API_KEY"),
        "geocode": toponym,
        "format": "json"
    }
    response = requests.get(GEOCODER_API_URL, params=params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_spns = toponym["boundedBy"]["Envelope"]
    spn1 = map(float, toponym_spns["lowerCorner"].split())
    spn2 = map(float, toponym_spns["upperCorner"].split())
    spn = ','.join([str(abs(next(spn1) - next(spn2))), str(abs(next(spn1) - next(spn2)))])
    coords = ','.join(toponym_coodrinates.split())

    params = {
        'spn': spn,
        "ll": coords,
        'l': maptype
    }
    print(maptype)
    response = requests.get(STATIC_API_URL, params=params)
    image = response.content
    print(response.url)
    with open('static/img/resp.jpg', 'wb') as img:
        img.write(image)
