#This is for the File-uploading into the Fast-APIs.

# from fastapi import FastAPI,UploadFile,File

# app = FastAPI(title="This is a demo for File Uploding API Pipeline",description="This is the Example for clearing the File-Uploading Concept of the Python.")

# @app.post("/upload")
# async def upload_file(file : UploadFile = File(...)):
    
#     return {"File Name":file.filename, "File Type": file.content_type}

from fastapi import FastAPI,UploadFile,File
import shutil

app = FastAPI(title="This is a demo for File Uploding API Pipeline",description="This is the Example for clearing the File-Uploading Concept of the Python.")

@app.post("/upload")
def upload_file(file : UploadFile = File(...)):

    with open(f"temp/uploded_{file.filename}","wb") as a:
        shutil.copyfileobj(file.file,a)
    
    return {"message":"File Successfuly uploaded."}