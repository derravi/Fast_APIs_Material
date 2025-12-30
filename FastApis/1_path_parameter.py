from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

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