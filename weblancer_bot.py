import json
import requests

from parser import get_new_jobs

URL = 'https://api.telegram.org/bot1146299123:AAHfQi6E8fabgO-NRMi--yU3gnP_C5rdT7g/sendMessage?parse_mode=HTML'
with open('data.json') as file:
    data = json.load(file)
    TOKEN = data['token']
    CHAT_ID = data['chat_id']


def create_msg(title, description, category, link, payment=''):
    msg = {
        'text':f"<b>{title}</b>\n{category} • {payment if payment else 'Цена не указана'}\n\n{description}\n\n{link}\n".encode('UTF-8'),
        'chat_id': CHAT_ID,
    }
    return msg


while True:
    jobs = get_new_jobs()

    if jobs:
        for job in jobs:
            title = '🔥' + job.find('a', {'class': 'text-bold show_visited'}).next_element + '🔥'
            description =  job.find('p', {'class': 'text_field'}).next_element
            category = job.find('div', {'class': 'col-sm-8 text-muted dot_divided'}).next_element.next_element.next_element
            link = 'https://www.weblancer.net' + job.find('a', {'class': 'text-bold show_visited'})['href']

            if job.find('div', {'class': 'float-right float-sm-none title amount indent-xs-b0'}):
                temp = job.find('div', {'class': 'float-right float-sm-none title amount indent-xs-b0'}).next_element.next_element.next_element
                payment = temp.strip() if '$' in temp else None

            response = requests.post(URL, create_msg(title, description, category, link, payment))
