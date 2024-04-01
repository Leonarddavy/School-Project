import mysql.connector



def connect_to_db():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port = 3306,
    database = "tender"
    )
    mycursor = mydb.cursor()
    