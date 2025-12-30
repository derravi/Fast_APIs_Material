#Field Velidator in the Pydentic.
"""
1. mode="before"
->Runs before Pydantic converts the input data into its declared type.
->Used to clean, modify, or preprocess raw input values.
->Example: Converting "25" → 25 before validation, or trimming extra spaces from a string.

2. mode="after"
->Runs after Pydantic converts the field into its declared type.
->Used to validate or check the final converted value.
->Example: Ensuring an integer value (like age) is between 1 and 100.

In Simple Words:
"before" → Prepare the data (works on raw input).
"after" → Check the data (works on the final, converted value).

"""

from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Optional,Annotated
class veriable_testing(BaseModel):

    name: str
    age:int
    email : EmailStr
    mobile_no : str

    @field_validator('email')
    @classmethod
    def email_velidator(cls,value):

        velid_domain = ['axis.com','icici.com']

        user_domain = value.split('@')[-1]

        if user_domain not in velid_domain:
            raise ValueError("Enter the velid Domain email id.")
        return value

    @field_validator('name')
    @classmethod
    def name_velidator(cls,value):
        return value.upper()
    
    @field_validator('mobile_no')
    @classmethod
    def number_velidation(cls,value):
        if len(value) != 10:
            raise ValueError("Enter the Velid Mobile number")
        return value 
    
    @field_validator('age',mode='after')
    @classmethod
    def age_velidation(cls,value):
        if 0 < value < 100:
            return value
        else:
            return ValueError("Enter the Velid Age.")


def patient_info(patient:veriable_testing):
    print("Name:",patient.name)
    print("Age:",patient.age)
    print("Email:",patient.email)
    print("Mobile No:",patient.mobile_no)
    
data = {'name':'Darpan','age':'21','email':'abcd@icici.com',"mobile_no":"1234867891"}

patient = veriable_testing(**data)

patient_info(patient)