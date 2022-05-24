from config import SCAN_BUFOR_FILE

class Buffer:
        
    def add_to_buffer(self, employee_id, scaner_id, scan_time):
        f = open(SCAN_BUFOR_FILE,"a")
        f.write(employee_id+", "+scaner_id+", "+scan_time+"\n")

    def red_from_buffer(self):
        f = self.fopen = open(SCAN_BUFOR_FILE,"r")
        return f.read().split("\n")
    