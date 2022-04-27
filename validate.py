from datetime import datetime, timedelta

def validate_data(data):
    now = datetime.now()
    creation_date = datetime.strptime(data['creation_date'], '%Y-%m-%d %H:%M:%S.%f')

    life_time = timedelta(minutes = int(data['life_time']))
    latest_date = creation_date + life_time
    earliest_date = creation_date - life_time
    
    if now < earliest_date or now > latest_date:
        return False
    
    return True
