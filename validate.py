from datetime import datetime, timedelta
from scaner_logger import Scaner_Logger

def validate_data(data):
    now = datetime.now()
    creation_date = datetime.strptime(
        data['creation_date'], '%Y-%m-%d %H:%M:%S.%f'
    )

    life_time = timedelta(minutes=int(data['life_time']))
    latest_date = creation_date + life_time
    earliest_date = creation_date - life_time

    if now < earliest_date or now > latest_date:
        logger = Scaner_Logger()
        logger.log_Info("QR code out of date")
        return False, "Kod QR nieaktualny"

    return True,""
