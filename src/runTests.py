from testHelper import TestHelper
import random
import json

#I know using unittests library would be more code efficient, but let's have some fun with it? ...

global tsi

#For tests 1(a) and 1(b)...
def login_test(flag):

    global tsi
    random_index       = random.randint(0, 5)
    sec_message        = None
    ver_user_email     = tsi.verified_user_emails[random_index]
    test_num           = "Test 1(a): Valid " if flag else "Test 1(b): Invalid "
    params             = {"email":ver_user_email, "password":"password"} if flag else {"email":ver_user_email} #For unverified user response test
    resp               = tsi.send_request(params, "login", "p")
    data, status_code  = None, resp.status_code
    #Check to make sure that a JSON response is even returned...
    try:
        data = resp.json()
    except ValueError:
        return json.dumps({f'{test_num}Login Submission Test':"Failed.  No JSON returned in server response."})
    
    #Now that we know a JSON response has been returned, we check formatting of response by first gathering our boolean checks...
    token_in_data, status_200 = "token" in data, status_code == 200 
    error_in_data, status_400 = "error" in data, status_code == 400

    response_is_correct      = (token_in_data and status_200) if flag else (error_in_data and status_400)
    if flag: sec_message     = "Incorrect format." if status_200 else "Incorrect status code."
    if not flag: sec_message = "Incorrect format." if status_400 else "Incorrect status code." 
    message                  = "Passed.  Correct response returned from server." if response_is_correct else f'Failed.  {sec_message}'
    return json.dumps({f'{test_num}Login Submission Test':message})

#For test 2(a)...
def users_list():

    global tsi 
    resp    = tsi.send_request({}, "users", "g")
    data    = None 
    message = None
    #Check to make sure that a JSON response is even returned...
    try:
        data = resp.json()
    except ValueError:
        return json.dumps({"Test 2(a): GET Users List Test": "Failed.  No JSON returned in server response."})
    #Now that we know a JSON response has been returned, we check the relevant formatting elements by first gathering our boolean checks...
    page_in_data, per_page_in_data     = "page" in data, "per_page" in data
    total_in_data, total_pages_in_data = "total" in data, "total_pages" in data 
    data_in_data, status_200           = "data" in data, resp.status_code == 200
    support_in_data                    = (("url" in data["support"] and "text" in data["support"]) if "support" in data else ("support" in data))
    #Here we perform the actual formatting checks...
    all_keys_in_data           = (page_in_data and per_page_in_data and total_in_data and total_pages_in_data and data_in_data and support_in_data)
    response_form_correct      = ((data["per_page"] == len(data["data"])) and data["total"] == (data["per_page"] * data["total_pages"])) if all_keys_in_data else all_keys_in_data
    sec_message                = "Inconsistent values provided in response." if (not response_form_correct and all_keys_in_data) else "Incorrect format."
    if status_200: message     = "Passed.  Correct response returned from server." if response_form_correct else f'Failed.  {sec_message}'
    if not status_200: message = "Failed.  Incorrect status code."
    return json.dumps({"Test 4(a): Get User List Test":message})
    
#For tests 3(a) and 3(b)...
def single_user(flag):

    global tsi 
    index    = str(random.randint(1, 6)) if flag else str(15)
    test_num = "Test 3(a): Valid " if flag else "Test 3(b): Invalid " 
    #We know there are 6 valid users per page, but in a real API test, we would have to ascertain this type of info first, obviously...
    resp = tsi.send_request({}, "users/" + index, "g")
    data = None
    #Check to make sure that JSON response is even returned...
    try:
        data = resp.json()
    except ValueError:
        return json.dumps({f'{test_num}Single User Test': "No JSON returned in server response."})
        
    #Now that we know a JSON response has been returned, we check the formatting by first gathering our boolean checks...
    #If flag is asserted, we perform the 3(a) test, else we perform the 3(b) test...
    data_in_data    = ("id" in data["data"] and "email" in data["data"] and "first_name" in data["data"] and "last_name" in data["data"] and "avatar" in data["data"]) if "data" in data else ("data" in data)
    support_in_data = ("url" in data["support"] and "text" in data["support"]) if "support" in data else ("support" in data)
    status_404      = resp.status_code == 404
    correct_length  = len(data) == 0
    
    response_correct  = (data_in_data and support_in_data) if flag else (status_404 and correct_length)
    sec_message       = "Incorrect format." if flag else "Length(user list) != 0 or incorrect status code."
    message           = "Passed.  Correct response returned from server." if response_correct else f'Failed.  {sec_message}.'
    return json.dumps({f'{test_num}Single User Test':message})

#For test 4(a)
def create_user():

    global tsi 
    resp = tsi.send_request({"name":"Cerebus", "job":"Being an aardvark."}, "users", "p")
    data = None 

    try:
        data = resp.json()
    except ValueError:
        return json.dumps({"Test 4(a): Create New User Test": "Failed.  No JSON returned in server response."})

    name_in_data, job_in_data, id_in_data = "name" in data, "job" in data, "id" in data
    createdAt_in_data, status_201         = "createdAt" in data, resp.status_code == 201

    all_keys_in_data           = (name_in_data and job_in_data and id_in_data and createdAt_in_data)
    response_form_correct      = (data["name"] == "Cerebus" and data["job"] == "Being an aardvark.") if all_keys_in_data else all_keys_in_data
    sec_message                = "Request data does not match response data." if all_keys_in_data else "Incorrect format."
    if status_201: message     = "Passed.  Correct response returned from server." if response_form_correct else f'Failed.  {sec_message}'
    if not status_201: message = "Failed.  Incorrect status code."
    return json.dumps({"Test 4(a): Create User Test":message}) 

#For test 5(a)
def delete_user():

    global tsi 
    id_number = str(random.randint(1, 6))
    resp = tsi.send_request({}, "users/" + id_number, "d")

    response_correct = resp.status_code == 204
    message = "Passed.  Correct response returned from server." if response_correct else "Failed.  Incorrect status code."
    return json.dumps({"Test 5(a): Delete User Test":message}) 

def main():
    global tsi 
    tsi = TestHelper()
    #Valid login test (Test 1(a)):
    print(str(login_test(1)))
    #Invalid login test: (Test 1(b)):
    print(str(login_test(0)))
    #Get users test (Test 2(a)):
    print(str(users_list()))
    #Valid single user test (Test 3(a))
    print(str(single_user(1)))
    #Invalid single user test (Test 3(b))
    print(str(single_user(0)))
    #Create user test (Test4(a))
    print(str(create_user()))
    #Delete user test (Test 5(a))
    print(str(delete_user()))

if __name__ == "__main__":
    main()
