from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from operations.router import router_marks, router_auth, router_mark_status, router_balance, router_stock
from scheduler.reports import get_kiz_report, get_report_status, get_report_file_id, get_file, save_data
from logger import cleanup_logs, logs_path
from operations.config import QUERY_EMITTED_CRON_HOUR, QUERY_EMITTED_CRON_MINUTE, QUERY_INTRODUCED_CRON_HOUR, \
    QUERY_INTRODUCED_CRON_MINUTE, REPORT_FILE_INTERVAL, REPORT_STATUS_INTERVAL, GET_FILE_INTERVAL, SAVE_DATA_INTERVAL

app = FastAPI(title='CZ API')

scheduler = AsyncIOScheduler()
scheduler.add_job(get_kiz_report, 'cron', ['INTRODUCED', '3461061226', 8], hour=QUERY_INTRODUCED_CRON_HOUR,
                  minute=QUERY_INTRODUCED_CRON_MINUTE)
scheduler.add_job(get_kiz_report, 'cron', ['EMITTED', '3461061226', 8], hour=QUERY_EMITTED_CRON_HOUR,
                  minute=QUERY_EMITTED_CRON_MINUTE)
scheduler.add_job(get_report_status, 'cron', minute=REPORT_STATUS_INTERVAL)
scheduler.add_job(get_report_file_id, 'cron', minute=REPORT_FILE_INTERVAL)
scheduler.add_job(get_file, 'cron', minute=GET_FILE_INTERVAL)
scheduler.add_job(save_data, 'cron', minute=SAVE_DATA_INTERVAL)
scheduler.add_job(cleanup_logs, 'interval', [logs_path, ], minutes=37400)
scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', include_in_schema=False)
async def welcome():
    return {
        'status': 200,
        'details': 'welcome to our api. Read the instructions and go ahead',
        'data': []
    }


app.include_router(router_marks)
app.include_router(router_auth)
app.include_router(router_mark_status)
app.include_router(router_balance)
app.include_router(router_stock)
