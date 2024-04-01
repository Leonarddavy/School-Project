
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

router_pred = APIRouter()
app = FastAPI()
model = joblib.load("D:\\Prog\\tendormodel2.joblib")

class ContractorInfoRow(BaseModel):
    county: str
    contractor: str
    ifmis: int
    project: str
    category: str
    department: str
    tendersum: str
    
class ContractorInfoRequest(BaseModel):
    contractorinfo: str
    
class ContractorInfoResponse(BaseModel):
    rows: List[ContractorInfoRow]      
    
class PredictionRequest(BaseModel):
    data: list
    
class PredictionResponse(BaseModel):
    prediction: str    


@router_pred.get("/qualification", response_class=HTMLResponse)
def qualification_page():
    return open("static/qualification.html").read()





def contract_prediction(inputData):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender")

    mycursor = mydb.cursor()
    
    query = "SELECT * FROM completed_records"
    mycursor.execute(query)
    originalDataset = mycursor.fetchall()
  
    
    df = pd.DataFrame(originalDataset, columns=["id","County", "Contractor", "Ifmis", "Department", "Project", "Category", "TenderSum", "ContractPeriod", "CompletionStatus", "Quality"])
   
    contractorDataset = df[df["Contractor"] == inputData[0]]
    predictedDataset = contractorDataset [['ContractPeriod', 'CompletionStatus', 'Quality']]
 
    
    # Encoding dictionary
    encoding_dict = {
        'ContractPeriod': {'Yes': 0, 'No': 1},
        'CompletionStatus': {'Completed': 0, 'Not Completed': 1},
        'Quality': {'Met': 0, 'Not Met': 1}
    }
    
    def encode_dataset(predictedDataset, encoding_dict):
        encoded_dataset = []
        for index, row in predictedDataset.iterrows():
            encoded_sample = []
            for feature_name, feature_value in row.items():
                encoded_sample.append(encoding_dict[feature_name][feature_value])
            encoded_dataset.append(encoded_sample)
        return encoded_dataset
    
    encoded_predictedDataset = encode_dataset(predictedDataset, encoding_dict)
    predict = model.predict(encoded_predictedDataset)
    
    prediction_list = [] 
    for row in encoded_predictedDataset:
        predict = model.predict([row])
        for item in predict:
            prediction_list.append(item)
            
    # Converting the list into strings
    converted_list = ['Yes' if item == 0 else 'No' if item == 1 else 'Consider' for item in prediction_list] 
    
    # Populating the Qualify column  
    contractorDataset['Qualify'] = converted_list
    
    # Determining Qualifications
    qualify_count = contractorDataset["Qualify"].value_counts(normalize=True)
    # breakpoint()
    if qualify_count.get("Yes", 0) >= 0.5:
        a = "Qualify"
        # import pdb; pdb.set_trace()
        return PredictionResponse(prediction= a)
    elif qualify_count.get("No", 0) > 0.51:
        b = "Doesnt Qualify"
        return PredictionResponse(prediction= b)
    else:
        c = "Consider"
        return PredictionResponse(prediction= c)
        
        

def dbinquiry(contractorinfo):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender")

    mycursor = mydb.cursor()
    selected_columns = "County, Contractor, IFMIS, Project, Category ,Department, Tender_Sum"  

    sql = f"SELECT {selected_columns} FROM completed_records WHERE Contractor = '{contractorinfo}'"


    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    rows = []
    
    
    if myresult:
        rows = [
            {
                'county': row[0],
                'contractor':row[1],
                'ifmis':row[2],
                'project':row[3],
                'category':row[4],
                'department':row[5],
                'tendersum':row[6]
               
            }
            
            for row in myresult
        ]
        
    
        # import pdb; pdb.set_trace()
        return ContractorInfoResponse(rows=rows)
        
    else:
        d = "Contractor information not found"
        return ContractorInfoResponse(info=d)
    

def client_contract_prediction(inputData):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tender")

    mycursor = mydb.cursor()
    
    query = "SELECT * FROM completed_records"
    mycursor.execute(query)
    originalDataset = mycursor.fetchall()
  
    
    df = pd.DataFrame(originalDataset, columns=["id","County", "Contractor", "Ifmis", "Department", "Project", "Category", "TenderSum", "ContractPeriod", "CompletionStatus", "Quality"])
   
    contractorDataset = df[df["Contractor"] == inputData[0]]
    predictedDataset = contractorDataset [['ContractPeriod', 'CompletionStatus', 'Quality']]
 
    
    # Encoding dictionary
    encoding_dict = {
        'ContractPeriod': {'Yes': 0, 'No': 1},
        'CompletionStatus': {'Completed': 0, 'Not Completed': 1},
        'Quality': {'Met': 0, 'Not Met': 1}
    }
    
    def encode_dataset(predictedDataset, encoding_dict):
        encoded_dataset = []
        for index, row in predictedDataset.iterrows():
            encoded_sample = []
            for feature_name, feature_value in row.items():
                encoded_sample.append(encoding_dict[feature_name][feature_value])
            encoded_dataset.append(encoded_sample)
        return encoded_dataset
    
    encoded_predictedDataset = encode_dataset(predictedDataset, encoding_dict)
    predict = model.predict(encoded_predictedDataset)
    
    prediction_list = [] 
    for row in encoded_predictedDataset:
        predict = model.predict([row])
        for item in predict:
            prediction_list.append(item)
            
    # Converting the list into strings
    converted_list = ['Yes' if item == 0 else 'No' if item == 1 else 'Consider' for item in prediction_list] 
    
    # Populating the Qualify column  
    contractorDataset['Qualify'] = converted_list
    
    # Determining Qualifications
    qualify_count = contractorDataset["Qualify"].value_counts(normalize=True)
    # breakpoint()
    if qualify_count.get("Yes", 0) >= 0.5:
        a = "Congragulations, You Have Qualified!"
        # import pdb; pdb.set_trace()
        return PredictionResponse(prediction= a)
    elif qualify_count.get("No", 0) > 0.51:
        b = "Unfortunately, You Have Not Qualified"
        return PredictionResponse(prediction= b)
    else:
        c = "Pending Review"
        return PredictionResponse(prediction= c)

