from config import ENTER, LEAVE, SCANER_ID
from decrypt import decryption
from validate import validate_data
from database import Database
from api import ScanerApi
from datetime import datetime
import json

if __name__ == '__main__':
    db = Database()
    api = ScanerApi()
    validated = False
    while True:
        try:
            validated = False
            encrypted = input('Zeskanuj kod QR\n')
            if not db.check_connection():
                continue
            data = decryption(encrypted)
            data = json.loads(data)

            data = validate_data(data, db)
            if not data:
                continue
            validated = True
        except TypeError and ValueError:
            print('Zeskanowano nieprawidłowy kod QR')


        if validated:
            try:
                api.sendPostRequestToApi(SCANER_ID,data['employee_id'],datetime.now())
            except:
                print('Błąd API')