import requests
import json
from fastapi import  Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os

from starlette import status


def auth_wrapper_lamda(chatId):
    return lambda: auth_wrapper(chatId)

def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    for _ in range(3):
        print("AUTH: ", auth)
        if auth.credentials == None: return 0
        try:
        # loop and wait until get response.
            moodle_url = f"{os.getenv("BASE_URL")}"
            #print(f"{moodle_url}")
            # API endpoint to get user info (adjust the endpoint as needed)
            api_endpoint = f"{moodle_url}/webservice/rest/server.php"
            moodle_url = api_endpoint + "?wstoken=" + str(auth.credentials) + "&moodlewsrestformat=json"
            functionname = "core_user_get_users_by_field"
            serverurl = moodle_url + '&wsfunction=' + functionname
            username=2
            params = {"field" : "id"}
            values = {}
            values["values[0]"] = username
            res = requests.post(serverurl, params=params, data=values)
            decode_res = res.content.decode('utf-8')
            print(decode_res)
            print(res.status_code)
            if res.status_code == 200:
                data = json.loads(decode_res)
                id = data[0]["id"]
                print("USER ID: ", id)
                return id
            else:
                raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=401, detail="Invalid token")
    return 0