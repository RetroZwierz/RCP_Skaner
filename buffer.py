from config import SCAN_BUFOR_FILE, EMPLOYEE_LAST_STATUS, ENTER, LEAVE
import fileinput
import os, sys
import fileinput, os, requests, sys
from api import ScanerApi

api = ScanerApi()

def add_to_buffer(employee_id, scaner_id, scan_time):
    f = open(SCAN_BUFOR_FILE, "a")
    f.write(employee_id+", "+scaner_id+", "+scan_time+"\n")


def read_from_buffer():
    f = open(SCAN_BUFOR_FILE, "r")
    return f.read().split("\n")

def send_from_buffer():
    if not os.path.exists(SCAN_BUFOR_FILE):
        os.mknod(SCAN_BUFOR_FILE)
    api_work = True
    #print("test")
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
                if response == None:
                    print(line.replace('\n',''))
                    api_work = False
                    continue
            except requests.exceptions.ConnectionError as ex:
                print(line.replace('\n',''))
                api_work = False
                continue
            except Exception as ex:
                print("TestEXc " + ex, file=sys.stderr)
            if not response['code'] == 200:
                print(line)
                
    #print("Test8", file=sys.stderr)
    fileinput.close()

def change_last_status(employee_id, new_status):
    if not os.path.exists(EMPLOYEE_LAST_STATUS):
        os.mknod(EMPLOYEE_LAST_STATUS)
    found = False
    for line in fileinput.input(EMPLOYEE_LAST_STATUS, inplace=1):
        if not line == "":
            values = line.split(", ")
            if values[0] == employee_id:
                found = True
                if not new_status == None:
                    if values[1].strip() == "status="+ENTER:
                        print(line.replace("status="+ENTER+'\n', "status="+new_status))
                    elif values[1].strip() == "status="+LEAVE:
                        print(line.replace("status="+LEAVE+'\n', "status="+new_status))
                    else:
                        print(line.replace('\n',''))
                elif values[1].strip() == "status="+ENTER:
                     print(line.replace("status="+ENTER+'\n', "status="+LEAVE))
                elif values[1].strip() == "status="+LEAVE:
                    print(line.replace("status="+LEAVE+'\n', "status="+ENTER))
                else:
                    print(line.replace('\n',''))
            else:
                print(line.replace('\n',''))
    fileinput.close()

    if not found:
        f = open(EMPLOYEE_LAST_STATUS, "a")
        if not new_status == None:
            f.write(employee_id+", status="+new_status+"\n")


def check_last_status(employee_id):
    f = open(EMPLOYEE_LAST_STATUS, "r")
    lines = f.read().split("\n")
    for line in lines:
        if not line == "":
            values = line.split(", status=")
            if values[0] == employee_id:
                return values[1].strip()
