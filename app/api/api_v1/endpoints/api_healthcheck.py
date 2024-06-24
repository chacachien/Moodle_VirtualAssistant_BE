from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    return {"message": "I'm alive!", "Version": "1.0.0"}


import httpx
import requests
import json
from datetime import timedelta, datetime
from typing import Annotated, Union, Any
from fastapi import APIRouter, Depends, HTTPException, Security

from pydantic import BaseModel
from sqlalchemy.orm import Session

# from passlib.context import CryptContext
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
# from jose import JWTError, jwt
from core.config import settings

# def decode_token( token):
#     try:
#         payload = jwt.decode(token, self.SECRET_KEY, algorithms = self.ALGORITHM)
#         username: str= payload.get('sub')
#         userid: int = payload.get('id')
        
#         return {'username': username, "userid": userid}
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except:
#         raise HTTPException(status_code=401, detail="Invalid token")
    

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


@router.get("/get_user_info")
async def get_user_info(user=Depends(auth_wrapper)):
    # Replace the URL with your Moodle site's URL
    # moodle_url = "http://localhost/moodle"

    # # API endpoint to get user info (adjust the endpoint as needed)
    # api_endpoint = f"{moodle_url}/webservice/rest/server.php"

    # moodle_url = api_endpoint + "?wstoken=" + token + "&moodlewsrestformat=json"
    # functionname = "core_user_get_users_by_field"   
    # serverurl = moodle_url + '&wsfunction=' + functionname
    # username='hs1'
    # params = {"field" : "username"}
    # values = {}
    # values["values[0]"] = username
    # res = requests.post(serverurl, params=params, data=values)
    print('USER: ', user)
    if user == "success":
        return "hehehe"
    else:
        return "huhuhu"