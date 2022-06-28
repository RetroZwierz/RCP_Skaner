SECRET_KEY = 'vpU=Xm=zAQEUoUOpXhJF4oRhJmCaTBTQQDwvH40L1lXT'
SALT = 'UWZUaldtWnE0dDd3IXolQw=='
IV = 'blpyNHU3eCFBJUQqRy1LYQ=='

SCANER_ID = '100'

ENTER = '2'
LEAVE = '3'

API_IP = '10.1.9.162'
API_PORT = '5000'

LOG_FILE = '/var/log/RCP/skaner.log'
#Przechowuje dane ze skanowania nie wysłane na api
SCAN_BUFOR_FILE ='/var/log/RCP/buffer.log'
#Przechowuje ostatni stan pracownika
EMPLOYEE_LAST_STATUS ='/var/log/RCP/employeelaststatus.log'

#Co ile ma wysyłać informacje do api o aktywnośći
HEART_BEAT_TIME = 15 #minutes
#Co ile ma próbować wysłać dane ze skanowania które nie zostały wysłane na api przez zerwane połączenie
SCAN_BUFFER_SEND_TIME = 60 #seconds
