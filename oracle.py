from constants import (
    ORACLE_HOST, ORACLE_PORT, SERVICE_NAME,
    ORACLE_USER, ORACLE_PASSWORD
)
import cx_Oracle

class Oracle:

    def __init__(self):
        dsn_tns = cx_Oracle.makedsn(ORACLE_HOST, ORACLE_PORT, service_name=SERVICE_NAME)
        self.conn = cx_Oracle.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=dsn_tns)
        print("connected")
