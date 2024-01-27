import joblib
import pandas as pd
import mysql.connector
import openpyxl

from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Response
from typing import Optional, List
from sklearn.preprocessing import LabelEncoder
from typing import List
from pydantic import BaseModel
from fastapi.responses import RedirectResponse


from fastapi import APIRouter
from report.report import router_rp
from dashboard.dashboard import router_dsb
from prediction.prediction import router_pred
from register.register import process_registration_data
from login.login import router_lg




#Instance of fastapi
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the trained model
model = joblib.load("D:\\Prog\\tendormodel2.joblib")

#Classes containing responses to & from static pages
class PredictionRequest(BaseModel):
    data: list

class PredictionResponse(BaseModel):
    prediction: str

class ContractorInfoRequest(BaseModel):
    contractorinfo: str

class ContractorInfoRow(BaseModel):
    county: str
    contractor: str
    ifmis: int
    project: str
    contract_period: str
    completion_status: str
    quality: str

class ContractorInfoResponse(BaseModel):
    rows: List[ContractorInfoRow]   
    
# Define a Pydantic model for request validation
class RegistrationData(BaseModel):
    fullname: str
    username: str
    email: str
    phonenumber: str
    password: str
    confirmpassword: str



 

#First navigation into the static pages
# @app.get("/", response_class=HTMLResponse)
# def read_root():
#     return open("static/dashboard.html").read()



#Registration process
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return open("static/register.html").read()

@app.get("/login", response_class=HTMLResponse)
async def login():
    print("llll")
    return open("static/login.html").read()

@app.post("/submit-registration")
async def submit_registration(data: RegistrationData):
    process_registration_data(data)
    print("done")
    # breakpoint()
    #return RedirectResponse(url="/login")
    return open("static/login.html").read()




   


#Including routers
app.include_router(router_dsb)
app.include_router(router_rp)
app.include_router(router_pred)



#Prediction
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    data = request.data

    # Access the input data
    inputData = data  
    
    originalDataset = pd.read_excel("D:\\Prog\\dataset2.xlsx")  
    
    contractorDataset = originalDataset[(originalDataset["Contractor"] == inputData[0])]
    predictedDataset = contractorDataset [['Completed within contract period', 'Completion Status', 'Quality Check']]
    
    
    
    # Encoding dictionary
    encoding_dict = {
        'Completed within contract period': {'Yes': 0, 'No': 1},
        'Completion Status': {'Completed': 0, 'Not Completed': 1},
        'Quality Check': {'Met': 0, 'Not Met': 1}
    }
    
    def encode_dataset(predictedDataset, encoding_dict):
        encoded_dataset = []
        for index, row in predictedDataset.iterrows():
            encoded_sample = []
            for feature_name, feature_value in row.items():
                encoded_sample.append(encoding_dict[feature_name][feature_value])
            encoded_dataset.append(encoded_sample)
        return encoded_dataset
    
    # Encode the dataset using the encoding dictionary
    
    encoded_predictedDataset = encode_dataset(predictedDataset, encoding_dict)
    
    
    predict = model.predict(encoded_predictedDataset)
    
    # Predicting the Qualify column 
    prediction_list = []
    for row in encoded_predictedDataset:
        predict = model.predict([row])
        for item in predict:
            prediction_list.append(item)
    
    
    # Converting the list into strings
    converted_list = ['Yes' if item == 0 else 'No' if item == 1 else 'Consider' for item in prediction_list] 
    
    
    # Populating the Qualify column  
    contractorDataset['Qualify'] = converted_list
    
    # import pdb;pdb.set_trace()
    # Determining Qualifications
    qualify_count = contractorDataset["Qualify"].value_counts(normalize=True)
    # import pdb;pdb.set_trace()
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
     



#Inquiring from db
@app.post("/getinfo", response_model=ContractorInfoResponse)
async def get_info(request: ContractorInfoRequest):
    contractorinfo = request.contractorinfo

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="tendor")

    mycursor = mydb.cursor()
    sql = f"SELECT * FROM contractor_information WHERE Contractor = '{contractorinfo}'"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    rows = []
    
    
    # import pdb; pdb.set_trace()
    if myresult:
        rows = [
            {
                'county': row[1],
                'contractor':row[2],
                'ifmis':row[3],
                'project':row[4],
                'contract_period':row[5],
                'completion_status':row[6],
                'quality':row[7]
               
            }
            
            for row in myresult
        ]
        # import pdb; pdb.set_trace()
        return ContractorInfoResponse(rows=rows)
        
    else:
        d = "Contractor information not found"
        return ContractorInfoResponse(info=d)

# Handle OPTIONS request for /predict endpoint
@app.options("/predict")
async def options_predict(response: Response):
    allowed_methods = ["POST", "OPTIONS"]  # Specify the allowed methods for the endpoint
    response.headers["Allow"] = ",".join(allowed_methods)
    response.headers["Access-Control-Allow-Origin"] = "*"  # Allow requests from any origin
    response.headers["Access-Control-Allow-Methods"] = ",".join(allowed_methods)
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response
