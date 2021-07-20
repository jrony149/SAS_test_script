import requests
import json

class TestHelper():

    def __init__(self):
        self.url                      = "https://reqres.in/api/"
        self.url2                     = "http://localhost:13801/SAS_test"
        self.response                 = requests.get(self.url + "users")
        self.verified_user_emails     = [self.response.json()["data"][x]["email"] for x in range(len(self.response.json()["data"]))]          
        self.non_verified_user_emails = ["unver1@yahoo.com", "unver2@gmail.com", "unver3@bunkmail.com", "unver4@hotmail.com", "unver5@yahoo.com", "unver6@gmail.com"]

    def send_request(self, params, endpoint, request_type):

        headers  = {'content-type':'application/json'}
        payload  = json.dumps(params)
        #target   = self.url + endpoint
        target   = self.url2
        response = None
        
        if request_type == "p":
            try: response = requests.post(url=target, data=payload, headers=headers, timeout=2)
            except requests.exceptions.Timeout: return json.dumps({"Timeout": "Failed.  Timeout occurred."})
        elif request_type == "g": 
            try: response = requests.get(url=target, data=payload, headers=headers, timeout=2)
            except requests.exceptions.Timeout: return json.dumps({"Timeout": "Failed.  Timeout occurred."})
        elif request_type == "d": 
            try: response = requests.delete(url=target, data=payload, headers=headers, timeout=2)
            except requests.exceptions.Timeout: return json.dumps({"Timeout": "Failed.  Timeout occurred."})
        
        return response

        
        