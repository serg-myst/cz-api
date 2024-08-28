from dotenv import load_dotenv
import os

load_dotenv()

URL_CZ = os.environ.get('URL_CZ')
URL_REPORT = os.environ.get('URL_REPORT')
URL_BALANCE = os.environ.get('URL_BALANCE')
URL_RESULT = os.environ.get('URL_RESULT')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
QUERY_INTRODUCED_CRON_HOUR = os.environ.get('QUERY_INTRODUCED_CRON_HOUR')
QUERY_INTRODUCED_CRON_MINUTE = os.environ.get('QUERY_INTRODUCED_CRON_MINUTE')
QUERY_EMITTED_CRON_HOUR = os.environ.get('QUERY_EMITTED_CRON_HOUR')
QUERY_EMITTED_CRON_MINUTE = os.environ.get('QUERY_EMITTED_CRON_MINUTE')
REPORT_STATUS_INTERVAL=os.environ.get('REPORT_STATUS_INTERVAL')
REPORT_FILE_INTERVAL=os.environ.get('REPORT_FILE_INTERVAL')
GET_FILE_INTERVAL=os.environ.get('GET_FILE_INTERVAL')
SAVE_DATA_INTERVAL=os.environ.get('SAVE_DATA_INTERVAL')
