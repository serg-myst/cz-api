from fastapi import APIRouter
from pydantic import BaseModel
import requests
import json
from fastapi import Depends
from .database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Token
from .config import URL_CZ

router_auth = APIRouter(
    prefix='/cz-auth',
    tags=['Auth']
)

router_marks = APIRouter(
    prefix='/marks-info',
    tags=['Marks']
)


@router_auth.get('/')
async def get_token(session: AsyncSession = Depends(get_async_session)):
    query = select(Token)
    result = await session.scalars(query)

    return {
        'status': 200,
        'details': '',
        'data': result.all()
    }


class Params(BaseModel):
    mark: str


@router_marks.post('/')
async def get_kiz_full_info(mark: Params, session: AsyncSession = Depends(get_async_session)):
    query = select(Token)
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

    body = [mark.mark[:31]]

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
