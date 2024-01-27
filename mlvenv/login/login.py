
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
router_lg = APIRouter()


@router_lg.get("/", response_class=HTMLResponse)
async def dashboard_page():
    return open("static/login.html").read()