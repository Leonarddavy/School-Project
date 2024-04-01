
import pandas as pd
import mysql.connector
import openpyxl
import hashlib
import hmac
import jwt

from fastapi import FastAPI



secret_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJc3N1ZXIgKGlzcykiOiJJc3N1ZXIiLCJJc3N1ZWQgQXQgKGlhdCkiOiIyMDI0LTAyLTAzVDA5OjE0OjU4LjEyMloiLCJTdWJqZWN0IChzdWIpIjoiU3ViamVjdCIsIlVzZXJuYW1lIChhdWQpIjoiSmF2YUd1aWRlcyIsIlJvbGUiOiJBRE1JTiJ9.PiK_jzwTqvFRuZOx0Z1PHZJXJnYL5aAgP2kZyottI00"

def hash_password(password, secret_key):
    # Create an HMAC object using SHA256 algorithm and the provided secret key
    h = hmac.new(secret_key.encode('utf-8'), digestmod=hashlib.sha256)
    h.update(password.encode('utf-8'))
    hashed_password = h.hexdigest()
    hashed_password = h.hexdigest()[:32]
    return hashed_password

def process_reset_data(datapsw):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()

    username_input = datapsw.Username
    password_input = hash_password(datapsw.Password, secret_key)
    cpassword_input = hash_password(datapsw.Cpassword, secret_key)

    # Assuming you have a table named 'registration'
    update_query = "UPDATE registration SET password = %s, confirmpassword = %s WHERE username = %s"

    # Note: You should handle exceptions and errors in a production environment.
    try:
        mycursor.execute(update_query, (password_input, cpassword_input, username_input))
        mydb.commit()
        # breakpoint()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        mycursor.close()
        mydb.close()

        
def process_clientreset_data(client_datapsw):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()

    username_input = client_datapsw.Username
    password_input = hash_password(client_datapsw.Password, secret_key)
    cpassword_input = hash_password(client_datapsw.Cpassword, secret_key)

    # Assuming you have a table named 'registration'
    update_query = "UPDATE contractor SET password = %s, cpassword = %s WHERE username = %s"

    # Note: You should handle exceptions and errors in a production environment.
    try:
        mycursor.execute(update_query, (password_input, cpassword_input, username_input))
        mydb.commit()
        # breakpoint()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        mycursor.close()
        mydb.close()

        