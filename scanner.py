from ast import Not
from config import SCANER_ID, ENTER, LEAVE
from decrypt import decryption
from validate import validate_data
from api import ScanerApi
from datetime import datetime, timedelta
from scaner_logger import Scaner_Logger
from buffer import add_to_buffer, change_last_status, check_last_status
import json
import requests

class Scanner:

    def __init__(self):
        self.api = ScanerApi()
        self.logger = Scaner_Logger()
        self.last_scan_time = None
        self.last_scan_code = None


    def scan(self, qrcode):
        validated = False
        try:
            validated = False
            data = decryption(qrcode)
            data = json.loads(data)

            validated,validate_message = validate_data(data)
            if not validated:
                return False, validate_message, None

        except TypeError and ValueError:
            return False, 'Nieprawidłowy kod QR', None


        if validated:
            try:
                now = datetime.now()
                if self.last_scan_time != None and self.last_scan_code != None:
                    if now <= self.last_scan_time + timedelta(seconds=10) and self.last_scan_code == qrcode:
                        last_status = check_last_status(data['employee_id'])
                        if last_status == '2':
                            last_status = "Ostatni status: Wejście"
                        elif last_status == '3':
                            last_status = "Ostatni status: Wyjście"
                        else:
                            last_status = ""
                        return False, 'Podwójny skan \n '+last_status, data['employee_id']
                self.last_scan_time = now
                self.last_scan_code = qrcode
                now = now.strftime('%Y-%m-%d %H:%M:%S')
                
                response = self.api.sendPostRequestToApi(SCANER_ID,data['employee_id'],now)

                if response == None:
                    self.logger.log_Error("API Connection Error host is unreachable\n")
                    change_last_status(data['employee_id'],None)
                    add_to_buffer(data['employee_id'],SCANER_ID,now)
                    last_status = check_last_status(data['employee_id'])
                    if last_status == ENTER:
                        return True, 'Zarejestrowano czas wejścia.', data['employee_id']
                    elif last_status == LEAVE:
                        return True, 'Zarejestrowano czas wyjścia.', data['employee_id']
                    else:
                        return False, 'Błąd komunikacji, spróbuj ponownie za chwilę.', None

                print(response)
                self.logger.log_Info("API Response: "+json.dumps(response)+"\n")

                if response['code'] == 200:
                    change_last_status(data['employee_id'],response['status'])
                    return True, response['data'], data['employee_id']
                else: 
                    return False, response['data'], data['employee_id']

            except requests.exceptions.ConnectionError as ex:
                self.logger.log_Error("API Connection Error "+str(ex)+"\n")
                change_last_status(data['employee_id'],None)
                add_to_buffer(data['employee_id'],SCANER_ID,now)
                last_status = check_last_status(data['employee_id'])
                if last_status == ENTER:
                    return True, 'Zarejestrowano czas wejścia.', data['employee_id']
                elif last_status == LEAVE:
                    return True, 'Zarejestrowano czas wyjścia.', data['employee_id']
                else:
                    return False, 'Błąd komunikacji, spróbuj ponownie za chwilę.', None
            except requests.Timeout as ex:
                self.logger.log_Error("API Connection Error "+str(ex)+"\n")
                change_last_status(data['employee_id'],None)
                add_to_buffer(data['employee_id'],SCANER_ID,now)
                last_status = check_last_status(data['employee_id'])
                if last_status == ENTER:
                    return True, 'Zarejestrowano czas wejścia.', data['employee_id']
                elif last_status == LEAVE:
                    return True, 'Zarejestrowano czas wyjścia.', data['employee_id']
                else:
                    return False, 'Błąd komunikacji, spróbuj ponownie za chwilę.', None
            except Exception as ex:
                return False, str(ex), None


            

