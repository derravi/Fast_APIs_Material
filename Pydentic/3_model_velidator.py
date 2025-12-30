
#Model Velidator in Pydentic
"""
Model Validator in Pydantic

->A Model Validator in Pydantic is used to validate the entire model after (or before) all fields are processed.
->It helps in applying cross-field validation — when one field’s rule depends on another field.

->mode="before" → Runs before data type conversion. Used to clean or modify raw input.
->mode="after" → Runs after data type conversion. Used to check final validated values.

Example use case:
->If a patient’s age is above 60, make sure an emergency contact is provided.

In short:
->Model Validator ensures logical consistency across multiple fields in the model.
"""
from pydantic import BaseModel,EmailStr,AnyUrl,Field,model_validator
from typing import Dict,Optional,Annotated
class veriable_testing(BaseModel):

    name:str 
    age:int
    email:EmailStr
    mo_no : int 
    weight:float
    married: bool
    contact_detail:Dict[str,str]

    @model_validator(mode='after')
    def validator_contact_information(cls,model):
        if model.age > 60 and "contect" not in model.contact_detail:
            raise ValueError("Paitent Older than 60 must have emergency contact details.")
        return model

def patient_info(patient:veriable_testing):
    print("Name:",patient.name)
    print("Age:",patient.age)
    print("Email is:",patient.email)
    print('Weight:',patient.weight)
    print("Married:",patient.married)
    print("Contact Details:",patient.contact_detail)

data = {
        'name':'Ravi',
        'age':'90',
        "email":'abcd@gmail.com',
        'mo_no':'1234567898',
        'weight':80.12,
        'married':True,
        'contact_detail':{'Country':'India','contect':'1234567894'}
        }

patient = veriable_testing(**data)

patient_info(patient)