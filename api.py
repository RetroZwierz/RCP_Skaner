from config import API_IP, API_PORT, SCANER_ID
import requests
import socket

class ScanerApi:

    def sendPostRequestToApi(self,scaner_id,card_id,time):
        response = requests.post("http://"+API_IP+":"+API_PORT+"/scan/", data = {'scaner_id':scaner_id,'card_id':card_id,'date_time':time}, timeout=2)
        return response.json()

    def sendScannerReport(self,time):
        response = requests.post("http://"+API_IP+":"+API_PORT+"/scannerreport/", data = {'scaner_id':SCANER_ID,'date_time':time}, timeout=2)
        return response.json()

    def sendTestRequestToApi():
        response = requests.get("http://"+API_IP+":"+API_PORT+"/test/")
        print(response.json())
    
    def checkHost(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((API_IP, int(API_PORT)))
            #s.shutdown(5)
            return True
        except Exception as ex:
            return False
        finally:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
