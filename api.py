from config import API_IP, API_PORT
import requests;

class ScanerApi:

    def sendTestRequestToApi():
        response = requests.get("http://127.0.0.1:5000/test/")
        print(response.json())

    def sendPostRequestToApi(self,scaner_id,employee_id,time):
        response = requests.post("http://"+API_IP+":"+API_PORT+"/scan/", data = {'scaner_id':scaner_id,'employee_id':employee_id,'date_time':time})
        return response.json()

    def registerAction():
        return 
    
    def watch():
        return