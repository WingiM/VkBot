import wikipedia
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from dotenv import load_dotenv
import os

load_dotenv('.env')
wikipedia.set_lang('ru')


def main():
    vk_session = vk_api.VkApi(token=os.getenv('TOKEN'))
    longpoll = VkBotLongPoll(vk_session, group_id=os.getenv("GROUP_ID"))
    work = False

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            user_id = event.obj.message['from_id']
            if work:
                msg = event.obj.message['text']
                try:
                    options = wikipedia.search(msg)
                    page = wikipedia.page(msg)
                    summ = wikipedia.summary(options[0])
                    message = f"{summ}\n\nПодробнее можно узнать на {page.url}"
                    vk.messages.send(user_id=user_id, message=message,
                                     random_id=random.randint(0, 2 ** 64))
                except wikipedia.exceptions.PageError:
                    vk.messages.send(user_id=user_id, message="Такой страницы на Википедии нет!",
                                     random_id=random.randint(0, 2 ** 64))
                except wikipedia.exceptions.DisambiguationError as e:
                    message = f"Попробуйте уточнить ваш запрос. Например, Уран -> Планета Уран/Элемент Уран"
                    vk.messages.send(user_id=user_id, message=message,
                                     random_id=random.randint(0, 2 ** 64))
                vk.messages.send(user_id=user_id, message="Напишите, что вы хотите, чтобы я нашел в википедии!",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=user_id, message="Напишите, что вы хотите, чтобы я нашел в википедии!",
                                 random_id=random.randint(0, 2 ** 64))
                work = True


if __name__ == '__main__':
    main()
