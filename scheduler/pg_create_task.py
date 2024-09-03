import requests
from requests.auth import HTTPBasicAuth
from pydantic import ValidationError
import json
from schemas import PG1C
from operations.config import BITRIX_HOOK
from operations.config import BASE_LIST, URL_1C


def create_task():

    for base in BASE_LIST.split(','):
        print(base)

    address = 'http://ks-1c.itv34.ru/VivoMarket/ru_RU/hs/Socialfood34/AllSkladsKindergarten'

    result = requests.post(address, auth=HTTPBasicAuth('Администратор'.encode('utf-8'), '20062006Sv!_'),
                           headers={'Authorization': 'Basic'})

    content = result.content.decode('utf-8')

    print(content)

    task_header = 'ЧЗ. Список товарных групп'
    task_body = ''

    response = [
        {
            'organisation': 'ООО Виво-Маркет',
            'pg': 'Молочная продукция',
            'mark_date': '01.01.2024'
        },
        {
            'organisation': 'ООО Виво-Маркет',
            'pg': 'Обувь',
            'mark_date': '01.01.2024'
        },
        {
            'organisation': 'ООО Виво-Маркет',
            'pg': 'Еще что-то',
            'mark_date': '01.01.2024'
        }
    ]

    for item in response:
        try:
            query = PG1C(**item)
        except ValidationError as err:
            print(f"pydantic validation error {err}")
        else:
            task_body += f'{query.organisation}:    {query.pg}\n'

    '''
    
    task = {
        'TITLE': task_header,
        "DESCRIPTION": task_body,
        "CREATED_BY": 1135,
        "RESPONSIBLE_ID": 1135,
        "AUDITORS": [
            1135
        ]
    }

    method = 'tasks.task.add'
    body = {'fields': task}
    result = requests.post(f'{BITRIX_HOOK}/{method}', json=body)

    if result.status_code == 200:
        response = result.json()
        print(response)
    else:
        print(result.text)
    '''


if __name__ == '__main__':
    create_task()
