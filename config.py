SECRET_KEY = 'vpU=Xm=zAQEUoUOpXhJF4oRhJmCaTBTQQDwvH40L1lXT'
SALT = 'UWZUaldtWnE0dDd3IXolQw=='
IV = 'blpyNHU3eCFBJUQqRy1LYQ=='

SCANER_ID = '2'

ENTER = '2'
LEAVE = '3'

API_IP = '10.1.9.161'
#API_IP = 'localhost'
API_PORT = '5000'

LOG_FILE = '/home/kuznia/skaner.log'
#Przechowuje dane ze skanowania nie wysłane na api
SCAN_BUFOR_FILE ='/home/kuznia/buffer.txt'
#Przechowuje ostatni stan pracownika
EMPLOYEE_LAST_STATUS ='/home/kuznia/employeelaststatus.txt'

#Co ile ma wysyłać informacje do api o aktywnośći
HEART_BEAT_TIME = 15 #minutes
#Co ile ma próbować wysłać dane ze skanowania które nie zostały wysłane na api przez zerwane połączenie
SCAN_BUFFER_SEND_TIME = 60 #seconds
