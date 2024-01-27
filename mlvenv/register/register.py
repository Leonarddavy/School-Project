import pandas as pd
import mysql.connector
import hashlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from sklearn.preprocessing import LabelEncoder
from pydantic import BaseModel
from fastapi.responses import RedirectResponse


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.responses import HTMLResponse
from fastapi import Response
from fastapi import APIRouter, Request
from jwt import PyJWTError
from login.login import router_lg



    
router_rg = APIRouter()
app = FastAPI()

 # Check if the username is unique in the database
def is_username_unique(username, cursor):
    cursor.execute("SELECT username FROM registration WHERE username = %s", (username,))
    return cursor.fetchone() is None

 # Hash the password using bcrypt
def hash_password(password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password



#Connect to the database with the registration data
def process_registration_data(data):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port = 3306,
    database = "tender"
    )
    mycursor = mydb.cursor()
    
    # Check if the username is unique in the database
    if not is_username_unique(data.username, mycursor):
        return open("static/login.html").read()

        
        
        
    hashed_password = hash_password(data.password)
    hashed_confirmpassword = hash_password(data.confirmpassword)    
    # import pdb; pdb.set_trace()
    
    #Insert the registration data into the database 
    sql = "INSERT INTO registration (fullname, username, email, phonenumber, password, confirmpassword) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (data.fullname, data.username, data.email, data.phonenumber, hashed_password, hashed_confirmpassword)
    
    
    mycursor.execute(sql, val)
    
    mydb.commit()
    mydb.close()



