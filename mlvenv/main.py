import joblib
import pandas as pd
import mysql.connector
import openpyxl

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Response
from typing import Optional, List
from sklearn.preprocessing import LabelEncoder
from typing import List
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from fastapi import Depends
from fastapi.responses import FileResponse
from fastapi import Cookie, Request, Response

from fastapi import APIRouter
from report.report import router_rp
from dashboard.dashboard import router_dsb
from prediction.prediction import router_pred
from register.register import process_registration_data
from login.login import router_lg
from login.login import process_login_data
from resetpassword.reset import process_reset_data
from resetpassword.reset import process_clientreset_data
from prediction.prediction import dbinquiry
from prediction.prediction import ContractorInfoRow
from prediction.prediction import ContractorInfoRequest
from prediction.prediction import ContractorInfoResponse
from dashboard.dashboard import process_contractor_data
from dashboard.dashboard import process_project_data
from dashboard.dashboard import process_service_data
from dashboard.dashboard import process_dept_data
from report.report import send_db_data
from prediction.prediction import contract_prediction
from register.register import process_client_data
from login.login import process_clientlogin_data
from dashboard.dashboard import process_tendersum_data
from dashboard.dashboard import process_completecount_data
from dashboard.dashboard import process_pendingcount_data
from dashboard.dashboard import process_countycount_data
from fastapi.middleware.cors import CORSMiddleware
from dashboard.dashboard import process_contract_info
from prediction.prediction import client_contract_prediction







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

    
# Define a Pydantic model for request validation
class RegistrationData(BaseModel):
    fullname: str
    username: str
    email: str
    phonenumber: str
    password: str
    confirmpassword: str
    
class LoginData(BaseModel):
    username: str
    password: str
    
class ClientLogin(BaseModel):
    username: str
    password: str
    
class PasswordData(BaseModel):
    Username: str
    Password: str
    Cpassword: str
  
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
    
class ClientData(BaseModel):
    organization: str
    county: str
    fullname: str
    username: str
    email: str
    phonenumber: int
    password: str
    confirmpassword: str
    
class ClientPasswordData(BaseModel):
    Username:str
    Password:str
    Cpassword:str
    
    
class ContractorInfo(BaseModel):
    organization: str

    




@app.get("/", response_class=HTMLResponse)
async def read_root():
    return open("static/home.html").read()

@app.get("/choose", response_class=HTMLResponse)
async def read_root():
    return open("static/choose.html").read()


#Admin
@app.get("/register", response_class=HTMLResponse)
async def read_root():
    # return open("static/register.html").read()
    return open("static/register.html", encoding="utf-8").read()


@app.get("/checkmail", response_class=HTMLResponse)
async def read_root():
    return open("static/checkmail.html").read()

@app.get("/login", response_class=HTMLResponse)
async def login():
    return open("static/login.html").read()

@app.get("/reset", response_class=HTMLResponse)
async def reset():
    return open("static/reset.html").read()


@app.get("/dashboard", response_class=HTMLResponse)
def read_root():
    return open("static/dashboard.html").read()

@app.get("/image", response_class=FileResponse)
async def image():
    return FileResponse("static/images/eye.png", media_type="image/png")

#Client
@app.get("/client_register", response_class=HTMLResponse)
async def read_root():
    return open("static/client_register.html").read()

@app.get("/client_login", response_class=HTMLResponse)
async def read_root():
    return open("static/client_login.html").read()

@app.get("/client_reset", response_class=HTMLResponse)
async def read_root():
    return open("static/client_reset.html").read()

@app.get("/client_qualification", response_class=HTMLResponse)
async def read_root():
    return open("static/client_qualification.html").read()

@app.get("/client_dashboard", response_class=HTMLResponse)
async def read_root():
    return open("static/client_dashboard.html").read()

@app.get("/home_choose", response_class=HTMLResponse)
async def read_root():
    return open("static/home_choose.html").read()

# Admin Registration   
@app.post("/submit-registration")
async def submit_registration(data: RegistrationData):
    is_registered = process_registration_data(data)

    if not is_registered:
        return JSONResponse(content={"message": "Registration failed"}, status_code=400)
    else:
        return JSONResponse(content={"message": "Registration successful"}, status_code=200)
  
  
#Client registration
@app.post("/client-registration")
async def client_registration(clientdata:ClientData):
    
    is_client_registered = process_client_data(clientdata)
    
    if not is_client_registered:
        return JSONResponse(content={"message": "Registration failed"}, status_code=400)
    else:
        return JSONResponse(content={"message": "Registration successful"}, status_code=200)
    
#Admin Log in   
@app.post("/login")
async def login(login_data: LoginData):
    is_login = process_login_data(login_data)
   
    if is_login == False:
        return JSONResponse(content={"message": "Login failed"}, status_code=400)
    else:
        return JSONResponse(content={"message": "Login succesfull"}, status_code=200)  
 
# Admin Reset password   
@app.post("/reset")
async def reset_password(datapsw: PasswordData):
    
    is_reset = process_reset_data(datapsw)
    
    if is_reset == True:
        return JSONResponse(content={"message": "Password reset successful"}, status_code=200)
    
    if is_reset == False:
        return JSONResponse(content={"message": "Password reset failed"}, status_code=400) 

    

#Client Login
@app.post("/client_login")
async def client_login(client_login: ClientLogin):
    
    is_client_login = process_clientlogin_data(client_login)
    
    if is_client_login == True:         
        return JSONResponse(content={"message": "Login successfull"})
    
    if is_client_login == False:
        return JSONResponse(content={"message": "failed"})        
    
# @app.get("/user_profile")
# async def get_cookie(request:Request):
#     user_cookie = request.cookies.get("user_cookie")
#     return {user_cookie}

# @app.post("/client_login")
# async def client_login(client_login: ClientLogin):
#     is_client_login, user = process_clientlogin_data(client_login)
    
#     if is_client_login:
#         response = JSONResponse(content={"message": "Login successfull"})
#         await set_cookie(response, user)
#         return response
#     else:
#         return JSONResponse(content={"message": "Failed to login"})

# async def set_cookie(response: JSONResponse, user: str):
#     response.set_cookie(key="user_cookie", value=user, path="/user_profile")  # Set the path explicitly

# #CORS settings
# origins = ["*"]  # Update this with the actual allowed origins for your application

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/user_profile")
# async def get_cookie(request: Request):
#     user_cookie = request.cookies.get("user_cookie")
#     return {"user_cookie": user_cookie}    # breakpoint()

    
@app.post("/client_reset")
async def reset_password(client_datapsw: ClientPasswordData):
     
    is_reset = process_clientreset_data(client_datapsw)
    
    if is_reset == True:
        return JSONResponse(content={"message": "Password reset successful"}, status_code=200)
    
    if is_reset == False:
        return JSONResponse(content={"message": "Password reset failed"}, status_code=400) 



#Admin Count
@app.post("/contractorcount")
async def contractor_count():
    # is_count = process_contractor_data()    
    return process_contractor_data()

@app.post("/projectcount") 
async def project_count():
    return process_project_data()   
    
@app.post("/servicecount") 
async def service_count():
    return process_service_data()     
    
@app.post("/deptcount") 
async def dept_count():
    return process_dept_data()   

@app.post("/tendersum") 
async def tender_count():
    return process_tendersum_data()  

@app.post("/completecount") 
async def complete_count():
    return process_completecount_data()    

@app.post("/pendingcount") 
async def pending_count():
    return process_pendingcount_data()  

@app.post("/countycount") 
async def county_count():
    return process_countycount_data() 

@app.post("/contract_info") 
async def contract_info(info: ContractorInfo):
    return process_contract_info(info)
 


#Admin report entry
@app.post("/sendinfo") 
async def send_inf(report: ReportData):
   
    is_sent = send_db_data(report)
 
    if is_sent == True:
        return JSONResponse(content={"message": "sent successfully"}, status_code = 200)
    
    if is_sent == False:
        return JSONResponse(content={"message": "records already exist"})
    
    if not is_sent[0]:
        return JSONResponse(content={"message": is_sent[1]}, status_code=is_sent[1])
        
    
    
    
#Including routers
app.include_router(router_dsb)
app.include_router(router_rp)
app.include_router(router_pred)



#Prediction
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    inputData = request.data 
    return contract_prediction(inputData)

#Client Qualification
@app.post("/client_predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    inputData = request.data 
    return client_contract_prediction(inputData)
     


#Admin Inquiring from db
@app.post("/getinfo", response_model=ContractorInfoResponse)
async def get_info(request: ContractorInfoRequest):
    contractorinfo = request.contractorinfo
    is_dbinquiry = dbinquiry(contractorinfo)
    return is_dbinquiry


# Handle OPTIONS request for /predict endpoint
@app.options("/predict")
async def options_predict(response: Response):
    allowed_methods = ["POST", "OPTIONS"]  # Specify the allowed methods for the endpoint
    response.headers["Allow"] = ",".join(allowed_methods)
    response.headers["Access-Control-Allow-Origin"] = "*"  # Allow requests from any origin
    response.headers["Access-Control-Allow-Methods"] = ",".join(allowed_methods)
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response
