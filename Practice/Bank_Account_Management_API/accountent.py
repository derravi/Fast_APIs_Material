from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from typing import Annotated,Dict,Optional
from fastapi.responses import JSONResponse
import json

try:

    app = FastAPI(title="Bank Account Management API")
except Exception as e:
    print(f"Error {e}.")

try:
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

except Exception as f:
    print(f"Error {f}.")

try:

    def load_data():
        with open('account.json','r') as f:
            return json.load(f)
except FileNotFoundError as e:
    print(f"Error {e}.")
except Exception as f:
    print(f"Error {f}")

try:
    def  save_data(data):
        with open('account.json','w') as g:
            json.dump(data,g)
except FileNotFoundError as e:
    print(f"Error {e}.")
except Exception as f:
    print(f"Error {f}")

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
        raise HTTPException(status_code=404,detail="Data not Existed")
    
    return data[account_no]

# @app.post("/add_acount",status_code=201)
# def add_account(account:account_details):

#     data = load_data()

#     if account.account_id in data:
#         raise HTTPException(status_code=400,detail="Account is alredy existed.")

#     data[account.account_id] = account.model_dump(exclude={"account_id"})

#     #save Data
#     save_data(data)

#     return JSONResponse(status_code=200,content={"message": "Account created successfully"})

@app.delete("/delete_account/{account_id}")
def del_account(account_id:str):

    try:
        data = load_data()
    except Exception as e:
        print(f"Error {e}")
    
    if account_id not in data:
        raise HTTPException(status_code=404,detail="Account data is not Existed.")
    
    del data[account_id]

    try:
        save_data(data)
    except Exception as e:
        print(f"Error {f}.")
    
    return JSONResponse(status_code=200,content={"message":"Account data is removed."})
