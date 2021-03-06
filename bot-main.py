import json

import wikipedia
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from dotenv import load_dotenv
import os
import requests
from geocoder import search

load_dotenv('.env')
wikipedia.set_lang('ru')


def get_photo():
    def auth_handler():
        key = input("Enter authentication code: ")
        remember_device = True

        return key, remember_device

    login, password = os.getenv("VK_LOGIN"), os.getenv("VK_PASSWORD")
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    upload = vk_api.VkUpload(vk_session)
    album_id, group_id = os.getenv('ALBUM_ID'), os.getenv("GROUP_ID")
    upload.photo(['static/img/resp.jpg'], album_id=album_id, group_id=group_id)
    album_id, group_id = os.getenv('ALBUM_ID'), os.getenv("GROUP_ID")
    response = vk.photos.get(album_id=album_id, group_id=group_id)
    if response['items']:
        photo = response['items'][-1]
        s = f'photo{photo["owner_id"]}_{photo["id"]}'
        return s


def main():
    vk_session = vk_api.VkApi(token=os.getenv('TOKEN'))
    longpoll = VkBotLongPoll(vk_session, group_id=os.getenv("GROUP_ID"))
    attach = False
    keyboard = {"one_time": True,
                "buttons": [
                    [
                        {
                            "action":
                                {"type": "text",
                                 "label": "Спутник",
                                 "payload": "{\"button\": \"sat\"}"}
                        },
                        {
                            "action":
                                {"type": "text",
                                 "label": "Гибрид",
                                 "payload": "{\"button\": \"skl\"}"}
                        },
                        {
                            "action":
                                {"type": "text",
                                 "label": "Карта",
                                 "payload": "{\"button\": \"map\"}"}
                        }
                    ]
                ]
                }
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if event.obj.message['text'].lower() == 'начать':
                vk.messages.send(user_id=event.obj.message['from_id'], random_id=random.randint(0, 2 ** 64),
                                 message="Напишите мне какое-нибудь место на Земле, а я вам его покажу!")
                attach = False
            elif not attach:
                name = event.obj.message['text']
                vk.messages.send(user_id=event.obj.message['from_id'], random_id=random.randint(0, 2 ** 64),
                                 keyboard=json.dumps(keyboard), message="Выберите, как отобразить картинку")
                attach = True
            else:
                search(name, event.obj.message['payload'].split(':')[1].rstrip('"}').lstrip('"'))
                vk.messages.send(user_id=event.obj.message['from_id'], random_id=random.randint(0, 2 ** 64),
                                 message=f"А вот и {name}", attachment=get_photo())
                attach = False


if __name__ == '__main__':
    main()
