from config import (
    ORACLE_HOST, ORACLE_PORT, SERVICE_NAME,
    ORACLE_USER, ORACLE_PASSWORD
)
import cx_Oracle


class Oracle:

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            dsn_tns = cx_Oracle.makedsn(
                ORACLE_HOST,
                ORACLE_PORT,
                service_name=SERVICE_NAME
            )
            self.pool = cx_Oracle.SessionPool(
                user=ORACLE_USER,
                password=ORACLE_PASSWORD,
                dsn=dsn_tns
            )
            print('Połączono z bazą danych Oracle')
            return True
        except cx_Oracle.DatabaseError:
            print('Połączenie z bazą danych Oracle nie powiodło się')
            return False

    def execute(self, sql, bindargs=None):
        try:
            connection = self.pool.acquire()
            cursor = connection.cursor()
            cursor.execute(sql, bindargs)
            connection.commit()
            self.pool.release(connection)
            return True
        except cx_Oracle.DatabaseError as error:
            print(error)

    def getOne(self, sql, bindargs=None):
        try:
            connection = self.pool.acquire()
            cursor = connection.cursor()
            result = cursor.execute(sql, bindargs).fetchone()
            self.pool.release(connection)
            return result
        except cx_Oracle.DatabaseError as error:
            print(error)

    def check_connection(self):
        try:
            connection = self.pool.acquire()
            connection.ping()
            return True
        except cx_Oracle.DatabaseError:
            return self.connect()
