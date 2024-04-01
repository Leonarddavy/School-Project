
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from sklearn.preprocessing import LabelEncoder
from typing import List
from pydantic import BaseModel
import mysql.connector
import openpyxl
from fastapi.responses import HTMLResponse
from fastapi import Response
from fastapi import APIRouter
from fastapi import HTTPException


class ReportData(BaseModel):
    county: str
    contractor: str
    ifmis: int
    department: str
    project: str
    category: str
    tender_sum:str
    contract_period: str
    completion_status: str
    quality: str
    

router_rp = APIRouter()
app = FastAPI()

# For example, you can define some additional routes or functions
@router_rp.get("/report", response_class=HTMLResponse)
def report_page():
    return open("static/report.html").read()


def send_db_data(report):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()

    try:
        # Extract data from the report
        county = report.county
        contractor = report.contractor
        ifmis = report.ifmis
        department = report.department
        project = report.project
        category = report.category
        tender_sum = report.tender_sum
        contract_period = report.contract_period
        completion_status = report.completion_status
        quality = report.quality

        # Check if records already exist based on unique fields (example: county, contractor, project)
        check_query = "SELECT * FROM completed_records WHERE county = %s AND contractor = %s AND project = %s AND ifmis = %s"
        check_values = (county, contractor, project, ifmis)
        mycursor.execute(check_query, check_values)
        existing_records = mycursor.fetchall()

        if existing_records:
            # Records already exist, handle it accordingly (return False and appropriate status code)
            return False 

        else:
            # Records don't exist, proceed with insertion
            insert_query = "INSERT INTO completed_records (county, contractor, ifmis, department, project, category, tender_sum, contract_period, completion_status, quality) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            insert_values = (county, contractor, ifmis, department, project, category, tender_sum, contract_period, completion_status, quality)
            mycursor.execute(insert_query, insert_values)
            mydb.commit()
            return True

    except Exception as e:
        print('Error:', e)
        # Failed to send data, return False and 500 status code
        raise HTTPException(status_code=500, detail='failed to send data')

    finally:
        mycursor.close()
        mydb.close()



        # breakpoint()
        
        
        
    