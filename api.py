from config import API_IP, API_PORT, SCANER_ID
import requests, sys;

class ScanerApi:

    def sendPostRequestToApi(self,scaner_id,employee_id,time):
        print("TestAPI", file=sys.stderr)
        response = requests.post("http://"+API_IP+":"+API_PORT+"/scan/", data = {'scaner_id':scaner_id,'employee_id':employee_id,'date_time':time})
        return response.json()

    def sendScannerReport(self,time):
        response = requests.post("http://"+API_IP+":"+API_PORT+"/scannerreport/", data = {'scaner_id':SCANER_ID,'date_time':time})
        return response.json()
    
    def sendScanDataFromBuffer(self,scaner_id,employee_id,time):
        response = requests.post("http://"+API_IP+":"+API_PORT+"/buffer/", data = {'scaner_id':SCANER_ID})
        return response.json()

    def sendTestRequestToApi():
        response = requests.get("http://"+API_IP+":"+API_PORT+"/test/")
        print(response.json())
