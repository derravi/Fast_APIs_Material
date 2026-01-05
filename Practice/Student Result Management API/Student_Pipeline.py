from fastapi import FastAPI,HTTPException
import json
from fastapi.responses import JSONResponse
from typing import Annotated
from pydantic import BaseModel,Field
from Data_Functions.data import load_data,save_data

#Pydantic model for student data

class Student_data(BaseModel):
    student_id:Annotated[str,Field(...,description="Enter the Student Id.",examples=["S001"])]
    student_name:Annotated[str,Field(...,description="Enter the Student Name:",examples=["Sanjay"])]
    maths_marks:Annotated[float,Field(...,description="Enter the marks of the Maths subject.",examples=[80.26])]
    science_marks:Annotated[float,Field(...,description="Enter the marks of the SciencE subject.",examples=[90.26])]
    English_marks:Annotated[float,Field(...,description="Enter the marks of the English subject.",examples=[69.26])]

app = FastAPI(title="Student Result Management Pipeline")

#Tesrting APis
@app.get("/")
def default():
    return {"message":"This is the Student Result Management Pipeline."}

#See the Data of the Student.
@app.get("/student_data")
def student_data():
    return load_data()

#See the Specific student details.
@app.get("/student_data/{student_id}")
def student_details(student_id:str):
    
    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=404,detail="Student Details is not existed.")
    
    return data[student_id]

#Add new data into the Student Pipeline
@app.post("/add_student")
def add_student(student:Student_data):

    data = load_data()

    if student.student_id in data:
        raise HTTPException(status_code=400,detail="Student data is existed.")
    
    data["student_id"] = student.model_dump(exclude="student_id")

    #save the data
    save_data(data)

    return JSONResponse(status_code=200,content={"message":"Data Successfuly Added."})