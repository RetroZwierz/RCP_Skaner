from config import SCANER_ID
from oracle import Oracle
from mysql_db import Mysql
from datetime import datetime


class Database:

    def __init__(self):
        self.mysql = Mysql()
        self.oracle = Oracle()

    def check_connection(self):
        if not self.mysql.check_connection():
            return False
        elif not self.oracle.check_connection():
            return False
        else:
            return True

    def validate_user(self, employee_id):
        query = ('SELECT czytnik, nr_karty FROM rcp_karty '
                 'WHERE oso_nr_ewidencyjny = :employee')
        return self.oracle.getOne(query, [employee_id])

    def get_last_action(self, employee_id):
        query = ("SELECT TRYB FROM rcp_rejestracje "
                 "WHERE oso_nr_ewidencyjny = :employee "
                 "ORDER BY czas DESC")
        return self.oracle.getOne(query, [employee_id])[0]

    def register_action(self, card_id, employee_id, action):
        now = datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        oracle_query = ("INSERT INTO rcp_rejestracje (nr_czytnika, nr_karty, czas, tryb, rodzaj, oso_nr_ewidencyjny, kon_kod, status_akutalizacji) "
                        "VALUES (:scaner, :card_id, to_date(:now, 'yyyy-mm-dd hh24:mi:ss'), :action, 0, :employee, 1, 'R')")
        mysql_query = ("INSERT INTO rcp_rejestracje (nr_czytnika, nr_karty, czas, tryb, rodzaj, nr_ewidencyjny) "
                       "VALUES (%s, %s, %s, %s, 0, %s)")
        success_mysql = True
        success_oracle = False 
        #success_mysql = self.mysql.execute(mysql_query, (SCANER_ID, card_id, now, action, employee_id))
        if success_mysql:
            success_oracle = self.oracle.execute(oracle_query, [SCANER_ID, card_id, now, action, employee_id])
        return (success_mysql, success_oracle)
