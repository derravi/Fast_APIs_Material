from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from typing import Annotated,Dict
from fastapi.responses import JSONResponse
import json

app = FastAPI(title="Bank Account Management API")

class account_details(BaseModel):
    account_id : Annotated[str,Field(...,description="Enter the Account ID",examples=["A001"])]
    name : Annotated[str,Field(...,description="Enter the name of the Accountent.",examples=["Harshil"])]
    balance : Annotated[float,Field(...,description="Enter the Balacne of the Account.",examples=[123.01])]
    gmail : Annotated[str,Field(...,description="Enter the Gmail of the Accountent.",examples=["abcd@gmail.com"])]
    password : Annotated[str,Field(...,description="Enter the Password of the Accountent.",examples=["password"])]

class dummy_account_details(BaseModel):
    name : Annotated[str,Field(...,description="Enter the name of the Accountent.",examples=["Harshil"])]
    balance : Annotated[float,Field(...,description="Enter the Balacne of the Account.",examples=[123.01])]
    gmail : Annotated[str,Field(...,description="Enter the Gmail of the Accountent.",examples=["abcd@gmail.com"])]

def load_data():
    with open('acount.json','r') as f:
        return json.load(f)

def  save_data(data):
    with open('acount.json','w') as g:
        json.dump(data,g)

@app.get("/")
def default():
    return {"message":"This is the Bank Account Management API pipeline."}

@app.get("/ac_details",response_model=Dict[str,dummy_account_details])
def ac_details():

    data = load_data()

    return data

@app.get("/ac_details/{account_no}",response_model=dummy_account_details)
def account_details(account_no:str):

    data = load_data()

    if account_no not in data:
        raise HTTPException(status_code=402,detail="Data not Existed")
    
    return data[account_no]

@app.post("/add_account")
def add_account(account:account_details):

    data = load_data()

    if account.account_id in data:
        raise HTTPException(status_code=400, detail="Data is Existed.")
    
    account_data = account.model_dump(exclude={"account_id"})

    data[account.account_id] = account_data

    save_data(data)

    return JSONResponse(status_code=200, content='Data Successfully Added.')
