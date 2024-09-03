from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update, delete
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
import requests
import json
import io, zipfile
import uuid
import shutil
import csv
import asyncio
from operations.models import ReportQuery as ReportQueryDB
from operations.models import CisStock as CisStock
from operations.database import async_session_maker
from scheduler.schemas import ReportQuery as ReportQueryPY
from scheduler.schemas import ReportQueryResponse as ReportQueryResponsePY
from scheduler.schemas import ReportQueryIdToDownload
from operations.config import URL_REPORT, URL_RESULT
from logger import log
from operations.token import get_token


async def add_query_to_db(query, table, get_item_list=False):
    async with async_session_maker() as session:
        try:
            if get_item_list:
                stmt = insert(table).values(query)
            else:
                stmt = insert(table).values(query.dict())
            do_update_stmt = stmt.on_conflict_do_nothing(index_elements=['id'])
            await session.execute(do_update_stmt)
            await session.commit()
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            raise RuntimeError(error) from e
        finally:
            await session.close()


async def update_query_to_db(obj, table, values: dict):
    async with async_session_maker() as session:
        try:
            stmt = update(table).where(table.report_id == obj.report_id).values(values)
            await session.execute(stmt)
            await session.commit()
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            raise RuntimeError(error) from e
        finally:
            await session.close()


async def get_kiz_report(status: str, inn: str, pg: int):
    token = await get_token()

    if token:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

        str_params = "{\"participantInn\": \"%1\",\"packageType\": [\"UNIT\"],\"status\": \"%2\"}"
        str_params = str_params.replace('%1', inn)
        str_params = str_params.replace('%2', status)

        body = {
            "format": "CSV",
            "name": "FILTERED_CIS_REPORT",
            "periodicity": "SINGLE",
            "productGroupCode": f"{pg}",
            "params": str_params
        }

        response = requests.post(URL_REPORT, headers=headers, json=body)

        # content = b'{"id":"1c662709-6f0c-488d-857b-78c90a8d8c1a","name":"FILTERED_CIS_REPORT","createDate":"2024-08-05T12:38:13.740","currentStatus":"PREPARATION","orgInn":"3461061226","periodicity":"SINGLE","productGroupCode":8,"timeoutSecs":300}'
        # content = b'{"id":"6aa0226b-ee87-4a26-9906-65716885cf40","name":"FILTERED_CIS_REPORT","createDate":"2024-08-07T13:13:04.306","currentStatus":"PREPARATION","orgInn":"3461061226","periodicity":"SINGLE","productGroupCode":8,"timeoutSecs":300}'

        if response.status_code != 200:
            log.error(
                f"query error. status {response.status_code}. message {response.json()}."
                f" query params: {status}; {inn}; {pg}")
        else:

            content = response.content

            content = json.loads(content.decode())

            try:
                query = ReportQueryPY(**content)
                query.cis_status = status
                log.info("pydantic schema OK")
            except ValidationError as err:
                log.error(f"pydantic validation error {err}")
            else:
                try:
                    log.info(f"Saving info in database ID = {query.report_id}")
                    await add_query_to_db(query, ReportQueryDB)
                except Exception as e:
                    log.error(f"Error saving info in database: {e}")


async def get_report_status():
    token = await get_token()

    if token:
        async with async_session_maker() as session:
            try:
                query = select(ReportQueryDB).where(ReportQueryDB.status_id == 1)
                result = await session.scalars(query)
                res = result.all()
            except SQLAlchemyError as e:
                error = str(e.__cause__)
                await session.rollback()
                log.error(f"get token error {e}")
                raise RuntimeError(error) from e
            finally:
                await session.close()

        for report in res:

            headers = {
                'Authorization': f'Bearer {token}'
            }

            response = requests.get(f'{URL_REPORT}/{report.report_id}?pg={report.pg_id}', headers=headers)

            if response.status_code != 200:
                log.error(f'error get report status {response.status_code}. text {response.text}')
            else:
                content = json.loads(response.content)
                try:
                    query = ReportQueryResponsePY(**content)
                    log.info("pydantic schema OK")
                except ValidationError as err:
                    log.error(f"pydantic validation error {err}")
                else:
                    try:
                        log.info(f"Saving info in database ID = {query.report_id}")
                        await update_query_to_db(query, ReportQueryDB,
                                                 {'status_id': query.status_id, 'status_date': query.status_date})
                    except Exception as e:
                        log.error(f"Error saving info in database: {e}")


async def get_report_file_id():
    token = await get_token()

    if token:
        async with async_session_maker() as session:
            try:
                query = select(ReportQueryDB).where(ReportQueryDB.status_id == 2).where(
                    ReportQueryDB.file_id == None)
                result = await session.scalars(query)
                res = result.all()
            except SQLAlchemyError as e:
                error = str(e.__cause__)
                await session.rollback()
                log.error(f"get token error {e}")
                raise RuntimeError(error) from e
            finally:
                await session.close()

        if res:
            id_str = ''
            for report in res:
                id_str += f'{report.report_id},'

            headers = {
                'Authorization': f'Bearer {token}'
            }

            response = requests.get(f'{URL_RESULT}/?page=0&pg=8&size=12&task_ids={id_str}', headers=headers)

            if response.status_code != 200:
                log.error(f'{response.status_code}. Error: {response.text}')
            else:
                content = json.loads(response.content)
                for task in content['list']:
                    try:
                        query = ReportQueryIdToDownload(**task)
                        log.info("pydantic schema OK")
                    except ValidationError as err:
                        log.error(f"pydantic validation error {err}")
                    else:
                        try:
                            log.info(f"Saving info in database ID = {query.report_id}")
                            await update_query_to_db(query, ReportQueryDB,
                                                     {'status_date': query.status_date,
                                                      'file_id': query.file_id,
                                                      'available_to_download': query.available_to_download,
                                                      'download_status': query.download_status})
                        except Exception as e:
                            log.error(f"Error saving info in database: {e}")


async def get_file():
    token = await get_token()

    if token:
        async with async_session_maker() as session:
            try:
                query = select(ReportQueryDB).where(ReportQueryDB.status_id == 2,
                                                    ReportQueryDB.file_id != None,
                                                    ReportQueryDB.available_to_download == 'AVAILABLE',
                                                    ReportQueryDB.file_data == None)
                result = await session.scalars(query)
                res = result.all()
            except SQLAlchemyError as e:
                error = str(e.__cause__)
                await session.rollback()
                log.error(f"get token error {e}")
                raise RuntimeError(error) from e
            finally:
                await session.close()

            if res:

                headers = {
                    'Authorization': f'Bearer {token}'
                }

                for report in res:
                    response = requests.get(f'{URL_RESULT}/{report.file_id}/file', headers=headers)
                    if response.status_code != 200:
                        log.error(f'{response.status_code}. Error: {response.text}')
                    else:
                        try:
                            log.info(f"Saving info in database ID = {report.report_id}")
                            await update_query_to_db(report, ReportQueryDB,
                                                     {'file_data': response.content})
                        except Exception as e:
                            log.error(f"Error saving info in database: {e}")


async def save_data():
    async with async_session_maker() as session:
        try:
            query = select(ReportQueryDB).where(ReportQueryDB.file_data != None,
                                                ReportQueryDB.save_to_table == False)
            result = await session.scalars(query)
            res = result.all()
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            log.error(f"get token error {e}")
            raise RuntimeError(error) from e
        finally:
            await session.close()

    for report in res:
        file_like_object = io.BytesIO(report.file_data)
        directory = str(uuid.uuid1())
        with zipfile.ZipFile(file_like_object, "a") as myzip:
            filename = myzip.infolist()[0].filename

        with zipfile.ZipFile(file_like_object, "r") as zf:
            zf.extractall(path=directory)

        stock_date = datetime.now()
        column_dict = {
            'cis': 0,
            'gtin': 1,
            'tnvedeaes': 2,
            'producerinn': 6,
            'ownerinn': 7,
            # 'prvetdocument': 8,
            'productname': 9,
            'brand': 10,
            'ownername': 11,
            'producername': 12,
            'status': 15,
            'emissiontype': 17,
            'packagetype': 19,
            'productgroup': 20,
            'introduceddate': 13,
            'applicationdate': 21,
            'emissiondate': 22,
            'expirationdate': 23,
            'productiondate': 27
        }
        item_list = []
        result_list = []

        EMPTY_DATE = datetime.strptime('01.01.2000 00:00:00', '%d.%m.%Y %H:%M:%S')

        with open(f'{directory}/{filename}', encoding='utf8',
                  newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            i = 0
            for row in reader:
                i += 1
                if i < 3:
                    continue
                item = {k: row[v] for k, v in column_dict.items()}
                item['stock_date'] = stock_date
                item['emissiondate'] = datetime.strptime(item['emissiondate'], "%Y-%m-%dT%H:%M:%S.%fZ")
                if report.cis_status == 'INTRODUCED':
                    item['introduceddate'] = datetime.strptime(item['introduceddate'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    item['applicationdate'] = datetime.strptime(item['applicationdate'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    item['expirationdate'] = datetime.strptime(item['expirationdate'], "%Y-%m-%dT%H:%M:%SZ")
                    item['productiondate'] = datetime.strptime(item['productiondate'], "%Y-%m-%dT%H:%M:%SZ")
                else:
                    item['introduceddate'] = EMPTY_DATE
                    item['applicationdate'] = EMPTY_DATE
                    item['expirationdate'] = EMPTY_DATE
                    item['productiondate'] = EMPTY_DATE

                item_list.append(item)
                if i == 1000:
                    result_list.append(item_list)
                    item_list = []
                    i = 0

            result_list.append(item_list)

            stmt = delete(CisStock).where(CisStock.status == report.cis_status)
            await session.execute(stmt)
            await session.commit()

            for item in result_list:
                try:
                    await add_query_to_db(item, CisStock, True)
                    log.info("Saving stocks info in database")
                except Exception as e:
                    log.error(f"Error saving info in database: {e}")

            await update_query_to_db(report, ReportQueryDB, {'save_to_table': True})

        try:
            shutil.rmtree(directory)
        except OSError as e:
            log.error(f'file delete error {directory}. error: {e}')


if __name__ == '__main__':
    ...
    # asyncio.run(get_kiz_report('INTRODUCED', '3461061226', 8))
    # asyncio.run(get_kiz_report('EMITTED', '3461061226', 8))
    # asyncio.run(get_report_status())
    # asyncio.run(get_report_file_id())
    # asyncio.run(get_file())
    # asyncio.run(save_data())
