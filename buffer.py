from config import SCAN_BUFOR_FILE, EMPLOYEE_LAST_STATUS, ENTER, LEAVE
import fileinput
import os, sys


def add_to_buffer(employee_id, scaner_id, scan_time):
    f = open(SCAN_BUFOR_FILE, "a")
    f.write(employee_id+", "+scaner_id+", "+scan_time+"\n")


def read_from_buffer():
    f = open(SCAN_BUFOR_FILE, "r")
    return f.read().split("\n")


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
        else:
            f.write(employee_id+", status="+ENTER+"\n")


def check_last_status(employee_id):
    f = open(EMPLOYEE_LAST_STATUS, "r")
    lines = f.read().split("\n")
    for line in lines:
        if not line == "":
            values = line.split(", status=")
            if values[0] == employee_id:
                return values[1].strip()
