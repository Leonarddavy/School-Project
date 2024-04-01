
import joblib
import pandas as pd
import mysql.connector
import openpyxl
import hashlib
import hmac
import jwt

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from sklearn.preprocessing import LabelEncoder
from typing import List
from pydantic import BaseModel

from fastapi.responses import HTMLResponse
from fastapi import Response
from fastapi import APIRouter


    


app = FastAPI()
router_lg = APIRouter()
secret_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJc3N1ZXIgKGlzcykiOiJJc3N1ZXIiLCJJc3N1ZWQgQXQgKGlhdCkiOiIyMDI0LTAyLTAzVDA5OjE0OjU4LjEyMloiLCJTdWJqZWN0IChzdWIpIjoiU3ViamVjdCIsIlVzZXJuYW1lIChhdWQpIjoiSmF2YUd1aWRlcyIsIlJvbGUiOiJBRE1JTiJ9.PiK_jzwTqvFRuZOx0Z1PHZJXJnYL5aAgP2kZyottI00"

 

# @router_lg.get("/", response_class=HTMLResponse)
# async def dashboard_page():
#     return open("static/login.html").read()

def hash_password(password, secret_key):
    # Create an HMAC object using SHA256 algorithm and the provided secret key
    h = hmac.new(secret_key.encode('utf-8'), digestmod=hashlib.sha256)
    h.update(password.encode('utf-8'))
    hashed_password = h.hexdigest()
    hashed_password = h.hexdigest()[:32]
    return hashed_password


def process_login_data(login_data):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port=3306,
            database="tender"
        )
        mycursor = mydb.cursor()

        username_input = login_data.username
        password_input = hash_password(login_data.password, secret_key)
        
        query = "SELECT username, password FROM registration WHERE username = %s"

        mycursor.execute(query, (username_input,))
        result = mycursor.fetchone()

        stored_username, stored_hashed_password = result if result else (None, None)

        # Use an if statement to check login credentials
        if stored_username == username_input and stored_hashed_password == password_input:
            return True
        else:
            return False
        
    except Exception as e:
        # Handle any exceptions that might occur during database interaction
        print(f"An error occurred: {e}")
        return False
    finally:
        # Make sure to close the database connection in the finally block
        mycursor.close()
        mydb.close()

        

def process_clientlogin_data(client_login):
    mydb = None
    mycursor = None
    
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port=3306,
            database="tender"
        )
        mycursor = mydb.cursor()

        username_input = client_login.username
        password_input = hash_password(client_login.password, secret_key)
        
        query = "SELECT username, password FROM contractor WHERE username = %s"

        mycursor.execute(query, (username_input,))
        result = mycursor.fetchone()

        stored_username, stored_hashed_password = result if result else (None, None)

        # Use an if statement to check login credentials
        if stored_username == username_input and stored_hashed_password == password_input:
            return True 
        else:
            return False        
        
    except Exception as e:
        # Handle any exceptions that might occur during database interaction
        print(f"An error occurred: {e}")
        return False
    
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()
