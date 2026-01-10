from fastapi import FastAPI,HTTPException
import json
from fastapi.responses import JSONResponse
from typing import Annotated,Optional,Dict
from pydantic import BaseModel,Field
from pydantic import computed_field

#Pydantic model for student data

class Student_data(BaseModel):
    student_id:Annotated[str,Field(...,description="Enter the Student Id.",examples=["S001"])]
    gmail:Annotated[str,Field(...,description="Enter the Gmail of the Student.",examples=["ravi123@gmail.com"])]
    password:Annotated[str,Field(...,description="Enter the Paswword of the student Acoount.",examples=["abcd@123"])]
    name:Annotated[str,Field(...,description="Enter the Student Name:",examples=["Sanjay"])]
    maths:Annotated[float,Field(...,le=100,description="Enter the marks of the Maths subject.",examples=[80.26])]
    science:Annotated[float,Field(...,le=100,description="Enter the marks of the SciencE subject.",examples=[90.26])]
    english:Annotated[float,Field(...,le=100,description="Enter the marks of the English subject.",examples=[69.26])]

class response_Student_data(BaseModel):
    student_id:Annotated[str,Field(...,description="Enter the Student Id.",examples=["S001"])]
    gmail:Annotated[str,Field(...,description="Enter the Gmail of the Student.",examples=["ravi123@gmail.com"])]
    name:Annotated[str,Field(...,description="Enter the Student Name:",examples=["Sanjay"])]
    maths:Annotated[float,Field(...,le=100,description="Enter the marks of the Maths subject.",examples=[80.26])]
    science:Annotated[float,Field(...,le=100,description="Enter the marks of the SciencE subject.",examples=[90.26])]
    english:Annotated[float,Field(...,le=100,description="Enter the marks of the English subject.",examples=[69.26])]

    @computed_field()
    @property
    def percentage(self) ->float:
        return round((self.maths+self.science+self.english)/3,2)
    
    @computed_field()
    @property
    def result(self)->str:
        if self.percentage >33.00:
            return "Pass"
        else:
            return "Fail"
        
def load_data():
    with open("student.json", "r") as f:
            return json.load(f)

def save_data(data):
    with open("student.json", "w") as g:
        json.dump(data, g, indent=4)
    

app = FastAPI(title="Student Result Management Pipeline")

#Tesrting APis
@app.get("/")
def default():
    return {"message":"This is the Student Result Management Pipeline."}

#See the Data of the Student.
@app.get("/student_data",response_model=Dict[str, response_Student_data])
def student_data():
    data = load_data()
    return data

#See the Specific student details.
@app.get("/student_data/{student_id}",response_model=response_Student_data)
def student_details(student_id:str):
    
    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=404,detail="Student Details is not existed.")
    
    return data[student_id]

#Add new data into the Student Pipeline
@app.post("/add_student", status_code=201)
def add_student(student: Student_data):
    data = load_data()

    if student.student_id in data:
        raise HTTPException(status_code=400, detail="Student already exists")

    data[student.student_id] = student.model_dump(exclude={"student_id"})
    save_data(data)

    return {"message": "Student data successfully added"}

#Update Endpoint

#Demo Optional duplicate model

class student_duplicate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    gmail:Annotated[Optional[str],Field(default=None)]
    maths:Annotated[Optional[float],Field(default=None)]
    science:Annotated[Optional[float],Field(default=None)]
    english:Annotated[Optional[float],Field(default=None)]

@app.post("/update_data/{student_id}")
def update_student(student_id: str, student_dummy_model: student_duplicate):

    # Load existing JSON data
    data = load_data()

    # Check student exists or not
    if student_id not in data:
        raise HTTPException(status_code=404,detail="Student data is not existed.")

    # Get existing student record
    existing_student_data = data[student_id]

    # Get only provided fields (PATCH behavior)
    update_student_data = student_dummy_model.model_dump()

    # Update existing fields
    for key, value in update_student_data.items():
        existing_student_data[key] = value

    # Add student_id back for Pydantic validation
    existing_student_data["student_id"] = student_id

    # Recreate Pydantic object (recalculates computed fields)
    student_pydantic_object = Student_data(**existing_student_data)

    # Save data INCLUDING computed fields
    data[student_id] = student_pydantic_object.model_dump(
        exclude={"student_id"},
        mode="json"
    )

    # Write back to JSON file
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Student data Successfully Updated."}
    )

#Delete Query
@app.delete("/Delete_student/{student_id}")
def delete_data(student_id:str):

    data =load_data()

    if student_id not in data:
        raise HTTPException(status_code=404,detail="Student data not existed.")
    
    del data[student_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message":"Student data is removed."})