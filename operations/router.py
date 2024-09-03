from fastapi import APIRouter
from pydantic import BaseModel
import requests
import json
from fastapi import Depends
from operations.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from operations.models import Token, KizStatus, CisStock
from operations.config import URL_CZ, URL_BALANCE, BITRIX_HOOK
import re
from operations.token import get_token
from operations.schemas import Task

router_auth = APIRouter(
    prefix='/cz-auth',
    tags=['Auth']
)

router_marks = APIRouter(
    prefix='/marks-info',
    tags=['Marks']
)

router_mark_status = APIRouter(
    prefix='/mark-status',
    tags=['Marks']
)

router_balance = APIRouter(
    prefix='/cz-balance',
    tags=['Balance']
)
router_stock = APIRouter(
    prefix='/cis-stock',
    tags=['Stock']
)

router_bitrix_task = APIRouter(
    prefix='/create-task',
    tags=['BITRIX']
)


@router_bitrix_task.post('')
def create_task(task: Task):
    method = 'tasks.task.add'
    body = {'fields': task.dict()}
    result = requests.post(f'{BITRIX_HOOK}/{method}', json=body)

    if result.status_code == 200:
        response = result.json()
        return {
            'status': 200,
            'details': '',
            'data': {'task_id': response['result']['task']['id']}
        }

    return {
        'status': result.status_code,
        'details': result.text,
        'data': ''
    }


# , offset: int = 0, limit: int = 500
@router_stock.get('/{status}')
async def get_stock(status: int, session: AsyncSession = Depends(get_async_session)):
    status_str = ''
    if status == 0:
        status_str = 'EMITTED'
    elif status == 2:
        status_str = 'INTRODUCED'

    query = select(CisStock).where(CisStock.status == status_str)  # .offset(offset).limit(limit)
    result = await session.scalars(query)

    return {
        'status': 200,
        'details': '',
        'data': result.all()
    }


@router_balance.get('/')
async def get_balance():
    token = await get_token()
    if token:

        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json'
        }

        response = requests.get(URL_BALANCE, headers=headers)

        if response.status_code != 200:

            return {
                'status': response.status_code,
                'details': response.text,
                'data': ''
            }

        else:
            data = json.loads(response.content)

            return {
                'status': response.status_code,
                'details': '',
                'data': data
            }


@router_mark_status.get('/')
async def get_mark_status(session: AsyncSession = Depends(get_async_session)):
    query = select(KizStatus)
    result = await session.scalars(query)

    return {
        'status': 200,
        'details': '',
        'data': result.all()
    }


@router_auth.get('/cz')
async def get_token_cz(session: AsyncSession = Depends(get_async_session)):
    query = select(Token).where(Token.token_type == 'CZ')
    result = await session.scalars(query)

    return {
        'status': 200,
        'details': '',
        'data': result.all()
    }


@router_auth.get('/suz')
async def get_token_suz(session: AsyncSession = Depends(get_async_session)):
    query = select(Token).where(Token.token_type == 'SUZ')
    result = await session.scalars(query)

    return {
        'status': 200,
        'details': '',
        'data': result.all()
    }


class Params(BaseModel):
    mark: str


def process_string(s):
    pattern = r'^(01\d{14}21.{6}(?=[^\w]|91|93)|01\d{14}21.{13}(?=[^\w]|91|93))'
    match = re.search(pattern, s)
    if match:
        return match.group(0)
    else:
        return None


@router_marks.post('/')
async def get_kiz_full_info(mark: Params, session: AsyncSession = Depends(get_async_session)):
    query = select(Token).where(Token.token_type == 'CZ')
    result = await session.scalars(query)
    res = result.first()
    token = res.jwt_token

    product_status = {
        1: 'Предметы одежды, бельё постельное, столовое, туалетное икухонное',
        2: 'Обувные товары',
        3: 'Табачная продукция',
        4: 'Духи и туалетная вода',
        5: 'Шины и покрышки пневматические резиновые новые',
        6: 'Фотокамеры (кроме кинокамер), фотовспышки и лампывспышки',
        8: 'Молочная продукция',
        9: 'Велосипеды и велосипедные рамы',
        10: 'Медицинские изделия',
        12: 'Альтернативная табачная продукция',
        13: 'Упакованная вода',
        14: 'Товары из натурального меха',
        15: 'Пиво, напитки, изготавливаемые на основе пива,слабоалкогольные напитки',
        16: 'Никотиносодержащая продукция',
        17: 'Биологически активные добавки к пище',
        19: 'Антисептики и дезинфицирующие средства',
        20: 'Корма для домашних животных (кромесельскохозяйственных) расфасованные в потребительскую упаковку',
        21: 'Морепродукты',
        22: 'Безалкогольное пиво',
        23: 'Соковая продукция и безалкогольные напитки',
        27: 'Игры и игрушки для детей',
        28: 'Радиоэлектронная продукция',
        31: 'Титановая металлопродукция',
        33: 'Растительные масла',
        34: 'Оптоволокно и оптоволоконная продукция',
        35: 'Парфюмерные и косметические средства и бытовая химия'
    }

    emission_type = {
        'LOCAL': 'Производство РФ',
        'FOREIGN': 'Ввезён в РФ',
        'REMAINS': 'Маркировка остатков',
        'CROSSBORDER': 'Ввезён из стран ЕАЭС',
        'REMARK': 'Перемаркировка',
        'COMMISSION': 'Принят на комиссию от физического лица'
    }

    status = {
        'EMITTED': 'Эмитирован',
        'APPLIED': 'Нанесён',
        'INTRODUCED': 'В обороте',
        'WRITTEN_OFF': 'Списан',
        'RETIRED': 'Выбыл',
        'WITHDRAWN': 'Выбыл',
        'DISAGGREGATION': 'Расформирован',
        'DISAGGREGATED': 'Расформирован',
        'APPLIED_NOT_PAID': 'Не оплачен'
    }

    package_type = {
        'UNIT': 'Единица товара (КИ)',
        'GROUP': 'Групповая упаковка (КИГУ)',
        'SET': 'Набор (КИН)',
        'BUNDLE': 'Комплект (КИК)',
        'BOX ': 'Транспортная упаковка (КИТУ)',
        'ATK': 'Агрегированный таможенный код (АТК)',
        'LEVEL1': 'Блок',
        'LEVEL2': 'Короб',
        'LEVEL3': 'Палета'
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }

    mark_pattern = process_string(mark.mark)

    if mark_pattern == None:
        return {
            'status': 500,
            'details': 'Марка не удовлетворяет заданному шаблону',
            'data': ''
        }

    body = [mark_pattern]

    response = requests.post(URL_CZ, headers=headers, json=body)
    content = json.loads(response.content)

    if response.status_code == 200:
        data = content[0].get('cisInfo')
        data['productGroup'] = product_status[data['productGroupId']]
        data['emissionType'] = emission_type[data['emissionType']]
        data['status'] = status[data['status']]
        data['packageType'] = package_type[data['packageType']]

        if data['child'] == []:
            data['child'] = 'Нет данных'

        return {
            'status': 200,
            'details': '',
            'data': data
        }
    else:
        return {
            'status': response.status_code,
            'details': content[0].get('errorMessage'),
            'data': ''
        }
