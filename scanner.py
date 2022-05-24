from config import SCANER_ID, LOG_FILE
from decrypt import decryption
from validate import validate_data
from api import ScanerApi
from datetime import datetime
from scaner_logger import Scaner_Logger
from buffer import Buffer
import json
import requests

class Scanner:

    def __init__(self):
        self.api = ScanerApi()
        self.logger = Scaner_Logger()
        self.buffer = Buffer()

    def scan(self, qrcode):
        validated = False
        try:
            validated = False
            print('Zeskanuj kod QR\n')
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
                self.logger.log_Info("API Response: "+response+"\n")
            except requests.exceptions.ConnectionError as ex:
                self.logger.log_Error("API Connection Error "+str(ex)+"\n")
                self.buffer.add_to_buffer(data['employee_id'],SCANER_ID,now)
                return 'Błąd połączenia z API'
                #print(buffer.red_from_buffer())
            except Exception as ex:
                return str(ex)


            

