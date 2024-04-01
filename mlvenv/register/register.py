import pandas as pd
import mysql.connector
import hashlib
import ssl
import smtplib
import random
import string
import hashlib
import hmac
import jwt

from email.message import EmailMessage
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from sklearn.preprocessing import LabelEncoder
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from email.message import EmailMessage

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.responses import HTMLResponse
from fastapi import Response
from fastapi import APIRouter, Request
from jwt import PyJWTError
from login.login import router_lg
# from connectiondb.connect_db import connect_to_db
# from connectiondb.connect_db import mycursor



    
router_rg = APIRouter()
app = FastAPI()
secret_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJc3N1ZXIgKGlzcykiOiJJc3N1ZXIiLCJJc3N1ZWQgQXQgKGlhdCkiOiIyMDI0LTAyLTAzVDA5OjE0OjU4LjEyMloiLCJTdWJqZWN0IChzdWIpIjoiU3ViamVjdCIsIlVzZXJuYW1lIChhdWQpIjoiSmF2YUd1aWRlcyIsIlJvbGUiOiJBRE1JTiJ9.PiK_jzwTqvFRuZOx0Z1PHZJXJnYL5aAgP2kZyottI00"

 # Check if the username is unique in the database
def is_username_unique(username, cursor):
    cursor.execute("SELECT username FROM registration WHERE username = %s", (username,))
    return cursor.fetchone() is None

def is_org_unique(orgname, cursor):
    cursor.execute("SELECT orgname FROM contractor WHERE orgname = %s", (orgname,))
    return cursor.fetchone() is None


 # Hash the password using bcrypt
def hash_password(password, secret_key):
    h = hmac.new(secret_key.encode('utf-8'), digestmod=hashlib.sha256)
    h.update(password.encode('utf-8'))
    hashed_password = h.hexdigest()
    hashed_password = h.hexdigest()[:32]
    return hashed_password


def generate_registration_link():
    # Generate a random registration token
    registration_token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    # Assuming your login page URL is '/login' (relative path)
    login_page_url = 'http://localhost:8000/client_login'
    
    # Construct the registration link with the token as a query parameter
    registration_link = f'{login_page_url}?token={registration_token}'
    
    return registration_link

def send_email(mailing):
    email_sender = 'dwavikoech@gmail.com'
    email_password = 'hote ngil knpk uzpy'
    email_receiver = mailing
    
    subject = "Registration"
    body = f''' 
    You have successfully registered! Click the following link to log in:
    
    {generate_registration_link()}
    '''
    
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
     
        
#Connect to the database with the registration data
def process_registration_data(data):
    # connect_to_db()
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
        return False
    
    hashed_password = hash_password(data.password, secret_key)
    hashed_confirmpassword = hash_password(data.confirmpassword, secret_key)    
    # import pdb; pdb.set_trace()
    
    #Insert the registration data into the database 
    sql = "INSERT INTO registration (fullname, username, email, phonenumber, password, confirmpassword) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (data.fullname, data.username, data.email, data.phonenumber, hashed_password, hashed_confirmpassword)
    
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    
    mailing = data.email
    send_email(mailing)
    return True

def process_client_data(clientdata):
    # connect_to_db()
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port = 3306,
    database = "tender"
    )
    mycursor = mydb.cursor()

    # Check if the username is unique in the database
    if not is_org_unique(clientdata.organization, mycursor):
        return False
    
    hashed_password = hash_password(clientdata.password, secret_key)
    hashed_confirmpassword = hash_password(clientdata.confirmpassword, secret_key)    
    # import pdb; pdb.set_trace()
    
    #Insert the registration data into the database 
    sql = "INSERT INTO contractor (orgname, county, fullname, username, email, phonenumber, password, cpassword) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (clientdata.organization, clientdata.county, clientdata.fullname, clientdata.username, clientdata.email, clientdata.phonenumber, hashed_password, hashed_confirmpassword)
    
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    
    mailing = clientdata.email
    send_email(mailing)
    return True


