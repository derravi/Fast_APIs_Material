#For Post Request.

"""
Path :- When we need to add some values into the browser url that time we are use this Path KeyWord from Pydentic.
Query :- Query tab use hota hai jab tumhe filter, sort, ya search karna hota hai.Ye optional ya configurable parameters hote hain.
Annotated:- Annotated ek Python 3.9+ feature hai jisko FastAPI ne adopt kiya hai
taaki Path, Query, Body, Header, etc. ko more readable aur reusable banaya ja sake.

"""
from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal

app = FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="Enter the Patient ID.",examples=["P001"])]
    name:Annotated[str,Field(...,description="Enter the name of the Patient.",examples=["Sachine vore"])]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Enter the Age of the Patient.",examples=["25"])]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Enter the Gender of the Patient.")]
    disease:Annotated[str,Field(...,description="Enter the Disease of the Patient.",examples=["Diabetes"])]
    hight:Annotated[float,Field(...,gt=0,description="Enter the hight of the Patient in mtrs.")]
    weight:Annotated[float,Field(...,gt=0,description="Enter the weight of the Patient in kg.")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.hight ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return "UnderWeight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "OverWeight"
        else:
            return "Obese"
@app.get("/")
def hello():
    return {'message':'Hello this is my first Apis.'}

@app.get("/about")
def about():
    return {'message':'My name is Der Ravi and I am Perchuing my M.Tech'}

def load_data():
    with open('Patiant.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('Patiant.json','w') as f:
        json.dump(data,f)

@app.get("/patient")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def patient_details(patient_id:str = Path(...,description="ID of the Patient in the DB",example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient data is not Found.")


@app.get('/sorted')
def sorted_field(sort_by :str = Query(...,description="Order Values based on the Hight,Weight and BMI."),order : str = Query('asc',description="Sort in asc or des order")):

    valid_field = ['hight','weight','bmi']

    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail=f"Enter the velid field from {valid_field}.")
    
    order_field = ['asc','desc']

    if order not in order_field:
        raise HTTPException(status_code=400,detail=f"Ente the Velid Order from the {order_field}.")
    
    data = load_data()

    sorted_order = True if order=='desc' else False

    sorted_data = sorted(data.values(),key=lambda x : x.get(sort_by,0),reverse=sorted_order)

    return sorted_data 

@app.post('/create')
def create_patient(patient:Patient):

    #Load the Json Data
    data = load_data()
    
    #Check if the Patient Id Is Exists in the data or not.
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient Alredy Exists.")
    
    #Add New Patient
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save into the 
    save_data(data)

    #Tell the Client your data is saved into the data.

    return JSONResponse(status_code=201,content={'message':'Patient Data Successfully Stored.'})