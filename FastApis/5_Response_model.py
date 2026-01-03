from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserDB(BaseModel):
    id:int
    name:str
    email:str
    password:str
    is_active:bool

class response_of_DB(BaseModel):
    id:int
    name:str
    email:str

@app.get("/user_data",response_model=response_of_DB)
def get_user_data():
    user_data = {
        "id": 1,
        "name": "Ravi",
        "email": "ravi@gmail.com",
        "password": "ravi@123",
        "is_active": True
    }

    return user_data