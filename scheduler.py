
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from api import ScanerApi
from buffer import read_from_buffer, change_last_status
from config import SCAN_BUFOR_FILE
import fileinput, os, requests, sys
import time

scheduler = BackgroundScheduler()
api = ScanerApi()


def start_scheduled_jobs():
    scheduler.start()
    print("I'm working...")


@scheduler.scheduled_job(IntervalTrigger(minutes=15))
def report_scanner_to_api():
    try:
        now = datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        response = api.sendScannerReport(now)
    except Exception as ex:
        print(str(ex))


@scheduler.scheduled_job(IntervalTrigger(seconds=5))
def send_data_from_buffer():
    if not os.path.exists(SCAN_BUFOR_FILE):
        os.mknod(SCAN_BUFOR_FILE)
    api_work = True
    for line in fileinput.input(SCAN_BUFOR_FILE, inplace=1):
        if not api_work:
            print(line.replace('\n',''))
            continue
        
        if True:
            values = line.split(", ")
            if not len(values) == 3:
                continue
            try:
                response = api.sendPostRequestToApi(values[1], values[0], values[2].replace('\n',''))
            except requests.exceptions.ConnectionError as ex:
                print(line.replace('\n',''))
                api_work = False
                continue
            except Exception as ex:
                print("TestEXc " + ex, file=sys.stderr)
            if response['code'] == 200:
                print("Test5", file=sys.stderr)
                #change_last_status(values[0], response['status'])
            else:
                print(line)
    print("Test8", file=sys.stderr)
    time.sleep(10)
    fileinput.close()
    print("Close")

    print("send scans stop")
