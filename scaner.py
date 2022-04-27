from sqlite3 import connect
from decrypt import decryption
from validate import validate_data
from oracle import Oracle
import json

if __name__ == '__main__':
    oracle_connection = Oracle()
    while True:
        encrypted = input()
        data = decryption(encrypted)
        data = json.loads(data)
        validation = validate_data(data)
        if validation:
            print('Dane poprawne')
        else:
            print('Dane niepoprawne')