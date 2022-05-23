import requests;

class ScanerApi:

    def sendTestRequestToApi():
        response = requests.get("http://127.0.0.1:5000/test/")
        print(response.json())

    def sendPostRequestToApi(self,scaner_id,employee_id,time):
        response = requests.post("http://127.0.0.1:5000/scan/", data = {'scaner_id':scaner_id,'employee_id':employee_id,'time':time})
        print(response.json())

    def registerAction():
        return 
    
    def watch():
        return