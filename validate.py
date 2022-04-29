from config import SCANER_ID
from datetime import datetime, timedelta


def validate_data(data, database):
    now = datetime.now()
    creation_date = datetime.strptime(
        data['creation_date'], '%Y-%m-%d %H:%M:%S.%f'
    )

    life_time = timedelta(minutes=int(data['life_time']))
    latest_date = creation_date + life_time
    earliest_date = creation_date - life_time

    if now < earliest_date or now > latest_date:
        print('Kod QR nieaktualny')
        return False

    employee_id = data['employee_id']
    scaner_id = database.validate_user(employee_id)

    if scaner_id is None:
        print('Użytkownik o podanym id nie istnieje')
        return False
    elif scaner_id[0] != SCANER_ID:
        print('Nie masz dostępu do tego czytnika')
        return False

    # TEMP oracle won't save otherwise
    data['card_id'] = scaner_id[1]

    return data
