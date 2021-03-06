import vk_api
from dotenv import load_dotenv
import os
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum'
load_dotenv('.env')


@app.route('/vk_stat/<int:id>')
def vk_stat(id):
    stats = get_stats(id)
    return render_template('vk_stat.html', stats=stats)


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def get_stats(group_id) -> dict:
    vk = vk_session.get_api()
    activity_fields = ['likes', 'comments', 'subscribed']
    ages_fields = ['12-18', '18-21', '21-24', '24-27', '27-30', '30-35', '35-45', '45-100']
    stats = {
        'activity': dict.fromkeys(activity_fields, 0),
        'ages': dict.fromkeys(ages_fields, 0),
        'cities': []
    }
    response = vk.stats.get(group_id=group_id, fields='reach')
    for i in response[:10]:
        activity = i.get('activity', {})
        reach = i.get('reach', {})

        ages = reach.get('age', {})
        cities = reach.get('cities', [])

        for action in activity:
            stats['activity'][action] += activity[action]

        for stat in ages:
            stats['ages'][stat['value']] += stat['count']

        for city in cities:
            stats['cities'].append(city['name'])
    return stats


if __name__ == '__main__':
    login, password = os.getenv("VK_LOGIN"), os.getenv("VK_PASSWORD")
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler
    )
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
    app.run()
