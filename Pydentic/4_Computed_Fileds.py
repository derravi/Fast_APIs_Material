"""
Computed Fields in Pydantic

->Computed Fields are used when you want to create a new field automatically based on the values of other fields — without user input.
->For example: If you have height and weight, you can automatically calculate BMI using them.
->This helps keep your data consistent and avoids manually calculating dependent values.
->You can define them using the @computed_field() decorator in Pydantic.
->Computed fields are read-only, meaning they are generated dynamically and not provided by the user.

In short:
->Computed Fields = Auto-calculated values inside the model (based on other fields).
"""

from pydantic import BaseModel,EmailStr,AnyUrl,Field,computed_field
from typing import List,Dict,Optional,Annotated

class veriable_testing(BaseModel):

    name:str 
    age:int
    email:EmailStr
    mo_no : int 
    weight:float #kg
    hight:float #mtrs
    married: bool
    contact_detail:Dict[str,str]

    @computed_field
    @property

    def bmi(self) -> float:
        bmi = round(self.weight/(self.hight**2),2)
        return bmi

def patient_info(patient:veriable_testing):
    print("Name:",patient.name)
    print("Age:",patient.age)
    print("Email is:",patient.email)
    print('Weight:',patient.weight)
    print('Hight:',patient.hight)
    print('BMI:',patient.bmi)
    print("Married:",patient.married)
    print("Contact Details:",patient.contact_detail)

data = {
        'name':'Ravi',
        'age':'90',
        "email":'abcd@gmail.com',
        'mo_no':'1234567898',
        'weight':85.12,
        'hight':1.2,
        'married':True,
        'contact_detail':{'Country':'India','contect':'1234567894'}
        }

patient = veriable_testing(**data)

patient_info(patient)