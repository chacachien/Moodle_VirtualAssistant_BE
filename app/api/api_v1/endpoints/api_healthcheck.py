from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    return {"message": "I'm alive!", "Version": "1.0.0"}


import httpx
import requests
import json
@router.get("/get_user_info")
async def get_user_info(token: str):
    # Replace the URL with your Moodle site's URL
    moodle_url = "http://localhost/moodle"

    # API endpoint to get user info (adjust the endpoint as needed)
    api_endpoint = f"{moodle_url}/webservice/rest/server.php"

    # Parameters for the API call
    # params = {
    #     "wstoken": token,
    #     "wsfunction": "core_user_get_users_by_id",
    #     "moodlewsrestformat": "json",
    #     "criteria[0][key]": "username",
    #     "criteria[0][value]": "desired_username",  # Replace with the desired username
    # }

    # async with httpx.AsyncClient() as client:
    #     response = await client.get(api_endpoint, params=params)
    #     print("RESPONSE: ", response)
    #     user_data = response.json()

    # return user_data

    moodle_url = api_endpoint + "?wstoken=" + token + "&moodlewsrestformat=json"
    functionname = "core_user_get_users_by_field"   
    serverurl = moodle_url + '&wsfunction=' + functionname
    username='hs1'
    params = {"field" : "username"}
    values = {}
    values["values[0]"] = username
    res = requests.post(serverurl, params=params, data=values)
    print(res)
    return json.loads(res.content)