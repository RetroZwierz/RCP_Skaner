
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
    #sys.stderr.write("your message")
    for line in fileinput.input(SCAN_BUFOR_FILE, inplace=1):
        print("debugging", file=sys.stderr)
        #sys.stderr.write("your message")
        if not api_work:
            print("API not work", file=sys.stderr)
            print(line.replace('\n',''))
            continue
        
        if True:
            values = line.split(", ")
            if not len(values) == 3:
                continue
            try:
                response = api.sendPostRequestToApi(values[1], values[0], values[2].replace('\n',''))
                print("Test2.1", file=sys.stderr)
            except requests.exceptions.ConnectionError as ex:
                print("Test3", file=sys.stderr)
                print(line.replace('\n',''))
                print("Test3.1", file=sys.stderr)
                api_work = False
                print("Test3.2", file=sys.stderr)
                continue
            except Exception as ex:
                print("TestEXc " + ex, file=sys.stderr)
            print("Test4", file=sys.stderr)
            if response['code'] == 200:
                print("Test5", file=sys.stderr)
                #change_last_status(values[0], response['status'])
                print("Test5.1", file=sys.stderr)
                print("Test5.2", file=sys.stderr)
            else:
                print("Test6", file=sys.stderr)
                print(line)
            print("Test7", file=sys.stderr)
    print("Test8", file=sys.stderr)
    time.sleep(10)
    fileinput.close()
    print("Close")

    print("send scans stop")
