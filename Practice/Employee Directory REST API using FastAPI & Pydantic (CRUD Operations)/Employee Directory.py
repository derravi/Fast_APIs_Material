from pydantic import BaseModel,Field,EmailStr
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated,Optional
import json


class Employee(BaseModel):
    id:Annotated[str,Field(...,description="Enter the Employee ID.",examples=["E001"])]
    name:Annotated[str,Field(...,description="Enter the name of the employee.",examples=["Shivam kumar"])]
    email:Annotated[str,Field(...,description="Enter the Email of the Employee.",examples=["abcd@gmail.com"])]
    department:Annotated[str,Field(...,description="Enter the Department of the Employee.",examples=["Backend Developer"])]
    role:Annotated[str,Field(...,description="Enter the role of the employee",examples=["Developing"])]
    date_of_joining:Annotated[str,Field(...,description="Enter the Joining date of the employee.",examples=["2022/12/12"])]
    is_active:Annotated[bool,Field(...,description="Enter the Active status of the employee.",examples=["True"])]

app = FastAPI()

#Load the Json file 
def load_data():
    with open("employee.json","r") as f:
        data = json.load(f)
    return data

#save data
def save_data(data):
    with open("employee.json","w") as f:
        json.dump(data,f)

#post and put endpoints.
@app.get("/")
def default():
    return {"message":"This is the Default message of the Employee Directory Api End points."}

#see the employee full data
@app.get("/employee")
def employee_data():

    data = load_data()

    return data

#see information of pertucular employee
@app.get("/employee/{emp_id}")
def employee_id(emp_id):

    data = load_data()

    if emp_id not in data:
        raise HTTPException(status_code=402,detail="Employee data not found.")
    
    return data[emp_id]

#Add the new Employess
@app.post("/employee_add/")
def add_employee(employee:Employee):

    data =load_data()

    if employee.id in data:
        raise HTTPException(status_code=400,detail="Employee data is alredy existed.")
    
    data[employee.id] = employee.model_dump(exclude=["id"])

    #Save data
    save_data(data)

    return JSONResponse(status_code=200,content={"message":"Data succesfully saved."})

#Put it means edit a Employee data.

class Employee_Demo(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    role: Optional[str] = None
    date_of_joining: Optional[str] = None
    is_active: Optional[bool] = None

#Put it means edit a Employee data.
@app.put("/employee_edit/{emp_id}")
def update_employee(emp_id: str, employee_update: Employee_Demo):

    data = load_data()

    # Check employee exists or not
    if emp_id not in data:
        raise HTTPException(status_code=404, detail="Employee not found.")

    # Existing employee data
    existing_employee_info = data[emp_id]

    # Only take fields which are sent in request
    updated_employee_info = employee_update.model_dump(exclude_unset=True)

    # Update only those fields
    for key, value in updated_employee_info.items():
        existing_employee_info[key] = value

    # Add id again for validation
    existing_employee_info["id"] = emp_id

    # Validate using main Employee model
    employee_pydantic_object = Employee(**existing_employee_info)

    # Remove id before saving (because id is key in JSON)
    data[emp_id] = employee_pydantic_object.model_dump(exclude=["id"])

    # Save updated data
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Employee data successfully updated."}
    )

@app.delete("/remove_patient/{patient_id}")
def remove_patient(patient_id:str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient nor existed.")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content="Patient Successfuly Removed.")