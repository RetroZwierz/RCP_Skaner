from config import ENTER, LEAVE
from decrypt import decryption
from validate import validate_data
from database import Database
import json

if __name__ == '__main__':
    db = Database()
    while True:
        try:
            encrypted = input('Zeskanuj kod QR\n')
            if not db.check_connection():
                continue
            data = decryption(encrypted)
            data = json.loads(data)

            data = validate_data(data, db)
            if not data:
                continue

            last_action = db.get_last_action(data['employee_id'])

            if last_action == ENTER:
                success_mysql, success_oracle = db.register_action(
                    data['card_id'],
                    data['employee_id'],
                    LEAVE
                )
                message = 'Sukces! Zarejestrowano czas wyjścia'
            else:
                success_mysql, success_oracle = db.register_action(
                    data['card_id'],
                    data['employee_id'],
                    ENTER
                )
                message = 'Sukces! Zarejestrowano czas wejścia'

            if not success_mysql:
                print("Błąd zapisu danych do bazy mysql")
                continue
            elif not success_oracle:
                print("Błąd zapisu danych do bazy oracle")
                continue

            print(message)
        except TypeError and ValueError:
            print('Zeskanowano nieprawidłowy kod QR')
