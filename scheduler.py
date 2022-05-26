
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from api import ScanerApi
from buffer import read_from_buffer, change_last_status,send_from_buffer
from config import SCAN_BUFOR_FILE,HEART_BEAT_TIME,SCAN_BUFFER_SEND_TIME
import fileinput, os, requests, sys
import time

scheduler = BackgroundScheduler()
api = ScanerApi()


def start_scheduled_jobs():
    scheduler.start()
    print("I'm working...")


@scheduler.scheduled_job(IntervalTrigger(minutes=HEART_BEAT_TIME))
def report_scanner_to_api():
    try:
        now = datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        response = api.sendScannerReport(now)
    except Exception as ex:
        print(str(ex))


@scheduler.scheduled_job(IntervalTrigger(seconds=SCAN_BUFFER_SEND_TIME))
def send_data_from_buffer():
    send_from_buffer()
