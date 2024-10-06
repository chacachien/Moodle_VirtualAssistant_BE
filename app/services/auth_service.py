
import httpx
import requests
import json
from datetime import timedelta, datetime
from typing import Annotated, Union, Any
from fastapi import APIRouter, Depends, HTTPException, Security

from pydantic import BaseModel
from sqlalchemy.orm import Session

from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer

from app.core.config import settings
import os 
def auth_wrapper_lamda(chatId):
    return lambda: auth_wrapper(chatId)

def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    try:
        #print("AUTH: ", auth) 
        moodle_url = f"{os.getenv("BASE_URL")}/moodle4113"
        #print(f"{moodle_url}")
        # API endpoint to get user info (adjust the endpoint as needed)
        api_endpoint = f"{moodle_url}/webservice/rest/server.php"

        moodle_url = api_endpoint + "?wstoken=" + str(auth.credentials) + "&moodlewsrestformat=json"
        functionname = "core_user_get_users_by_field"   
        serverurl = moodle_url + '&wsfunction=' + functionname
        username=1
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
    except:
        pass
    return 0