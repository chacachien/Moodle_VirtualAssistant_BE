
import httpx
import requests
import json
from datetime import timedelta, datetime
from typing import Annotated, Union, Any
from fastapi import APIRouter, Depends, HTTPException, Security

from pydantic import BaseModel
from sqlalchemy.orm import Session

from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer

from core.config import settings


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    try:
        print("AUTH: ", auth) 
        moodle_url = "http://localhost/moodle"

        # API endpoint to get user info (adjust the endpoint as needed)
        api_endpoint = f"{moodle_url}/webservice/rest/server.php"

        moodle_url = api_endpoint + "?wstoken=" + str(auth.credentials) + "&moodlewsrestformat=json"
        functionname = "core_user_get_users_by_field"   
        serverurl = moodle_url + '&wsfunction=' + functionname
        username='hs1'
        params = {"field" : "username"}
        values = {}
        values["values[0]"] = username
        res = requests.post(serverurl, params=params, data=values)
        print('status: ', res.status_code)
        if res.status_code == 200:
            return "success"
    except:
        pass
    return "fail"