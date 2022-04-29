from config import (
    MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD,
    MYSQL_DATABASE
)
import mysql.connector


class Mysql:

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
            )
            print('Połączono z bazą danych mysql')
        except mysql.connector.Error:
            print('Połączenie z bazą danych mysql nie powiodło się')

    def check_connection(self):
        if not self.db.is_connected():
            self.connect()
            return self.db.is_connected()
        return True

    def execute(self, sql, bindargs=None):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, bindargs)
            self.db.commit()
            return True
        except mysql.connector.Error as error:
            print(error)

    def getAll(self, sql, bindargs=None):
        try:
            cursor = self.db.cursor()
            return cursor.execute(sql, bindargs).fetchall()
        except mysql.connector.Error as error:
            print(error)

    def getOne(self, sql, bindargs=None):
        try:
            cursor = self.db.cursor()
            return cursor.execute(sql, bindargs).fetchone()
        except mysql.connector.Error as error:
            print(error)
