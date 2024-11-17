import requests
import json
from fastapi import  Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os

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

from app.models.base_model import get_default_datetime
from app.models.message_model import *
import os
from datetime import datetime
import json
import asyncpg
from fastapi import HTTPException
from starlette import status
from app.chatbot.model import ChatBot

class AuthService(object):
    def __init__(self):
        pass

    # Function to create a connection to the database
    @staticmethod
    async def get_db_connection():
        try:
            # Adjust the database connection settings accordingly
            connection = await asyncpg.connect(
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                database=os.getenv("POSTGRES_DB"),
                host=os.getenv("POSTGRES_SERVER"),
                port=os.getenv("POSTGRES_PORT")
            )
            return connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection error")

    # Function to close the connection
    @staticmethod
    async def close_db_connection(connection):
        try:
            await connection.close()
        except Exception as e:
            print(f"Error closing the database connection: {e}")

    # Function to get chat history without ORM
    @staticmethod
    async def get_token(userId: int):
        connection = await AuthService.get_db_connection()
        try:
            # Execute the SQL query to fetch the chat history
            query = """
                    SELECT token 
                    FROM mdl_external_tokens 
                    WHERE userid = $1 
                      AND externalserviceid = 2 
                      AND (validuntil = 0 OR extract(epoch from now()) < validuntil)
                    ORDER BY timecreated DESC;
                """
            token = await connection.fetchrow(query, userId)
            # Convert the fetched records into a list of dictionaries
            return token
        except Exception as e:
            print(f"Error fetching chat history: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            # Close the database connection
            await AuthService.close_db_connection(connection)