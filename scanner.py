from config import SCANER_ID
from decrypt import decryption
from validate import validate_data
from api import ScanerApi
from datetime import datetime
from scaner_logger import Scaner_Logger
from buffer import add_to_buffer, change_last_status
import json
import requests

class Scanner:

    def __init__(self):
        self.api = ScanerApi()
        self.logger = Scaner_Logger()

    def scan(self, qrcode):
        validated = False
        try:
            validated = False
            data = decryption(qrcode)
            data = json.loads(data)

            validated,validate_message = validate_data(data)
            if not validated:
                return False, validate_message

        except TypeError and ValueError:
            return False, 'Nieprawidłowy kod QR'


        if validated:
            try:
                now = datetime.now()
                now = now.strftime('%Y-%m-%d %H:%M:%S')
                response = self.api.sendPostRequestToApi(SCANER_ID,data['employee_id'],now)
                print(response)
                self.logger.log_Info("API Response: "+json.dumps(response)+"\n")

                if response['code'] == 200:
                    change_last_status(data['employee_id'],response['status'])
                    return True, response['data']
                else: 
                    return False, response['data']
            except requests.exceptions.ConnectionError as ex:
                self.logger.log_Error("API Connection Error "+str(ex)+"\n")
                change_last_status(data['employee_id'],None)
                add_to_buffer(data['employee_id'],SCANER_ID,now)
                return False, 'Błąd połączenia z API'
                #print(read_from_buffer())
            except Exception as ex:
                return False, str(ex)


            
