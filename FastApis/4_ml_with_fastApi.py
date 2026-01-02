from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
import pickle
from typing import Annotated
import pandas as pd

with open('model.pkl','rb') as f:
    model = pickle.load(f)

app = FastAPI()

#Make The Pydantic Model For User Input
class UserInput(BaseModel):
    Area_sqft:Annotated[float,Field(...,gt=0,description="Enter the Area of the House (in Square foot).",examples=[123.25])]
    Bedrooms:Annotated[int,Field(...,gt=0,description="Enter the Total number of Bedrooms.",examples=[4])]
    Bathrooms:Annotated[float,Field(...,gt=0,description="Enter the Total Number of Bathrooms.",examples=[1.0])]
    Floors:Annotated[float,Field(...,gt=0,description="Enter the Number of Floors.",examples=[1])]
    Year_Built:Annotated[int,Field(...,gt=0,description="Enter the Birth Year of the House.",examples=[2019])]

@app.get("/")
def root():
    return {"message": "Welcome to the House Price Prediction API!"} 

@app.post("/predict")
def predict_premium(data:UserInput):
    df = pd.DataFrame([{
        "Area_sqft": data.Area_sqft,
        "Bedrooms": data.Bedrooms,
        "Bathrooms": data.Bathrooms,
        "Floors": data.Floors,
        "Year_Built": data.Year_Built
    }])

    prediction = model.predict(df)[0][0]

    return JSONResponse(status_code=200,content={"predicted_price": float(round(prediction, 2)),
                                                 "message": f"The estimated price of the house is ₹{round(prediction,2)}"})

