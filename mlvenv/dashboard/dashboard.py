
import joblib
import pandas as pd
import mysql.connector
import openpyxl

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
router_dsb = APIRouter()


@router_dsb.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    return open("static/dashboard.html").read()

def process_contractor_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()

    table_name = 'records'
    column_name = 'Contractor'

    query = f"SELECT COUNT({column_name}) FROM {table_name}"
    mycursor.execute(query)
    result = mycursor.fetchone()
    
    mycursor.close()
    mydb.close()

    count = result[0]
    return count


    
def process_project_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()
    table_name = 'records'
    column_name = 'Project'

    query = f"SELECT COUNT({column_name}) FROM {table_name}"
    mycursor.execute(query)
    result = mycursor.fetchone()
    
    mycursor.close()
    mydb.close()

    count = result[0]
    return count


def process_service_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()
    table_name = 'records'
    column_name = 'Category'

    query = f"SELECT COUNT({column_name}) FROM {table_name}"
    mycursor.execute(query)
    result = mycursor.fetchone()
    
    mycursor.close()
    mydb.close()

    count = result[0]
    return count
    
def process_dept_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()
    table_name = 'records'
    column_name = 'Department'

    query = f"SELECT COUNT({column_name}) FROM {table_name}"
    mycursor.execute(query)
    result = mycursor.fetchone()
    
    mycursor.close()
    mydb.close()

    count = result[0]
    return count    

def process_contract_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()

    table_name = 'records'
    column_name = 'Contractor'

    query = f"SELECT COUNT({column_name}) FROM {table_name}"
    mycursor.execute(query)
    result = mycursor.fetchone()
    
    mycursor.close()
    mydb.close()

    count = result[0]
    return count


def process_tendersum_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()

    table_name = 'completed_records'
    column_name = 'Tender_Sum'

    query = f"SELECT {column_name} FROM {table_name}"

    mycursor.execute(query)
    results = mycursor.fetchall()  # Use fetchall() to get all rows

    values = [float(result[0].replace(',', '')) for result in results]  # Extracting values from each row

    total_sum = sum(values)  # Add all the numbers
    total_sum_str = '{:,.4f}'.format(total_sum)

    mycursor.close()
    mydb.close()
    return total_sum_str

def process_completecount_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()

    table_name = 'completed_records'
    column_name = 'Completion_Status'

    query = f"SELECT COUNT({column_name}) FROM {table_name} WHERE {column_name} = 'Completed'"

    mycursor.execute(query)
    result = mycursor.fetchone()
    
    mycursor.close()
    mydb.close()
    count = result[0]
    return count

def process_pendingcount_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()

    table_name = 'completed_records'
    column_name = 'Completion_Status'

    query = f"SELECT COUNT({column_name}) FROM {table_name} WHERE {column_name} = 'Not Completed'"

    mycursor.execute(query)
    result = mycursor.fetchone()
    
    mycursor.close()
    mydb.close()
    count = result[0]
    return count

def process_countycount_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()

    table_name = 'completed_records'
    column_name = 'County'

    query = f"SELECT {column_name} FROM {table_name}"

    mycursor.execute(query)
    results = mycursor.fetchall()
    
    unique_counties = set(result[0] for result in results)
    count_of_counties = len(unique_counties)
    
    mycursor.close()
    mydb.close()
    return count_of_counties


def process_contract_info(info):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender"
    )
    mycursor = mydb.cursor()

    table_name = 'completed_records'
    tender_sum_column = 'Tender_Sum'
    contractor_name = 'Contractor'
    orgname = info.organization
    column_index_to_select_tender_sum = 7
    column_index_to_select_contracts = 2
    column_index_to_select_projects = 5
    column_index_to_select_category = 6
    column_index_to_select_department = 4

    # Use parameterized query to prevent SQL injection
    query = f"SELECT * FROM {table_name} WHERE {contractor_name} = %s"
    mycursor.execute(query, (orgname,))  # Pass orgname as a parameter
    results = mycursor.fetchall()   # Use fetchall() to get all rows
    
    #Tender_Sum
    selected_column_values_tender_sum = [result[column_index_to_select_tender_sum] for result in results]
    # Extracting values from each row and handling ',' in the numbers
    converted_values = [float(value.replace(',', '')) if value is not None else None for value in selected_column_values_tender_sum]
    total_sum = sum(converted_values)  # Add all the numbers
    total_sum_str = '{:,.2f}'.format(total_sum)
    
    #Contracts
    selected_column_values_contracts = [result[column_index_to_select_contracts] for result in results]
    count_of_contracts = sum(1 for value in selected_column_values_contracts if value is not None)
    
    #Projects
    selected_column_values_projects = [result[column_index_to_select_projects] for result in results]
    all_projects = [str(value) for value in selected_column_values_projects if value is not None]
    count_of_projects = len(all_projects)
    
    #Category
    selected_column_values_category = [result[column_index_to_select_category] for result in results]
    all_categories = [str(value) for value in selected_column_values_category if value is not None]
    count_of_categories = len(all_categories)
    
    #Departments
    selected_column_values_department = [result[column_index_to_select_department] for result in results]
    all_departments = [str(value) for value in selected_column_values_department if value is not None]
    count_of_departments = len(all_departments)
    
    
    return count_of_contracts,total_sum_str, count_of_projects, count_of_categories, count_of_departments

    
    
    

    
 

