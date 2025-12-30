"""
1️⃣Field Validation

Create a Pydantic model Student with fields:

name (string)

age (integer, must be > 10)

email (EmailStr)

marks (float between 0–100)

👉 Validate that all fields are correct and print "Student data is valid!" when successful.


from pydantic import BaseModel,EmailStr,field_validator
import json
class student_fields(BaseModel):
    name:str
    age:int
    email: EmailStr
    marks:float

    @field_validator('marks')
    @classmethod
    def marks_checking(cls,value):
        if value >= 0 and value <= 100:
            return value
        else:
            raise ValueError("Enter the Velid Marks.")

def Student1(student: student_fields):
    print("Name:", student.name)
    print("Age:", student.age)
    print("Email:", student.email)
    print("Marks:", student.marks)
    
data = {
    "name": "Ravi Kumar",
    "age": 21,
    "email": "ravi.kumar@example.com",
    "marks": 87.5
}

Student = student_fields(**data)

Student1(Student)
"""

"""
2️⃣ Custom Field Validator

Write a model Employee that validates:

email must end with @company.com

mobile_no must be 10 digits only
If validation fails → raise ValueError("Invalid email or mobile number")


from pydantic import BaseModel,EmailStr,field_validator

class fields(BaseModel):
    name:str
    age:int
    email:EmailStr

    @field_validator('email')
    @classmethod
    def email_checker(cls,value):
        domain_value = ['company.com']
        temp = value.split("@")[-1]
        if temp not in domain_value:
            raise ValueError("Enter the velid Domain....")
        return value
    
def Employee(employee:fields ):
    print("Name:",employee.name)
    print("Age:",employee.age)
    print("Email id:",employee.email)

data = {'name':"Rohan",'age':50,'email':'abcd@company.com'}

data_object = fields(**data)
Employee(data_object)
"""

"""
3️⃣ Model Validator

Create a model BankAccount with:

name

age

balance
If age < 18 and balance > 0, raise error "Minor cannot have account balance!"


from pydantic import BaseModel,model_validator

class Bank(BaseModel):
    name:str
    age:int
    balance:float

    @model_validator(mode='after')
    def model_checker(cls,model):
        if model.age < 18 and model.balance > 0:
            raise ValueError("Minor cannot have account balance.")
        return model

def BankAccount(bank:Bank):
    print("Name:",bank.name)
    print("Age",bank.age)
    print("Balance:",bank.balance)

data = {'name':'ninja','age':20,'balance':1}

data_dict = Bank(**data)

BankAccount(data_dict)
"""

"""
4️⃣ Computed Field

Create a Person model with fields:

name, weight, height
Add a computed field bmi and print "BMI of <name> is <bmi>".


from pydantic import BaseModel,computed_field

class Person(BaseModel):
    name:str
    weight:float
    hight:float

    @computed_field 
    @property

    def bmi(self) -> float:
        bmi = self.weight/(self.hight**2)
        bmi = round(bmi,2)
        return bmi
    
def Student(student:Person):
    print("Hight",student.hight)
    print("Weight",student.weight)
    print("BMI",student.bmi)

data = {'name':'Sanjay','hight':2.5,'weight':80.25}

data_dict = Person(**data)
Student(data_dict)
"""

"""
5️⃣ Nested Model

Make a model Company with:

name

location (another model Address having city, state, pincode)
Print both company name and full address.


from pydantic import BaseModel

class Adress(BaseModel):
    city:str
    state:str
    pincode:int

class Company(BaseModel):
    name:str
    adress:Adress

def company_details(company:Company):
    print("Name:",company.name)
    print("City:",company.adress.city)
    print("State:",company.adress.state)
    print("Pincode:",company.adress.pincode)

adress_data = {'city':'Bhuj','state':'Gujarat',"pincode":123654}
adress_object = Adress(**adress_data)

company_data = {'name':'Kalpesh','adress':adress_object}
company_data_object=Company(**company_data)
company_details(company_data_object) 
"""

"""
6️⃣ Optional + AnyUrl

Make a model Portfolio with:

name

linkedin (Optional[AnyUrl])
If LinkedIn is missing, print "No LinkedIn link provided."


from pydantic import BaseModel,AnyUrl
from typing import Optional

class Portfolio(BaseModel):
    name:str
    linkedin:Optional[AnyUrl] = 'https://www.linkedin.com/in/ravi-kumar'

def portfolio(fetures:Portfolio):
    print("Name:",fetures.name)
    print("Linkedin Link:",fetures.linkedin)

data = {'name':'Rupesh','linkedin':'https:www.linkedin.com/in/ravi-kumar'}
data_object = Portfolio(**data)
portfolio(data_object)
"""

"""
7️⃣ Annotated + Field

Create a model Product with:

name: Annotated[str, Field(max_length=20)]

price: Annotated[float, Field(gt=0)]
Validate and print product info.


from pydantic import BaseModel,Field
from typing import Annotated

class Product(BaseModel):
    name: Annotated[str, Field(max_length=20)]
    price: Annotated[float,Field(gt=0)]

def product_details(product:Product):
    print("Name:",product.name)
    print("Price:",product.price)

data = {'name':'Mukesh','price':10}
data_object = Product(**data)

product_details(data_object)
"""

"""
8️⃣ Field Validator (mode="before")

Make a model User where:

age might come as string like "25".
Use mode="before" to convert it to integer automatically.

from pydantic import BaseModel,field_validator

    age:int

    @field_validator('age',mode='before')
    @classmethod

    def age_checker(cls,value):
        if isinstance(value,str):
            return int(value)
        return value

def User(user:User_veriable):
    print("Age",user.age)

data = {'age':'21'}
data_object = User_veriable(**data)
User(data_object)
class User_veriable(BaseModel):
"""

"""
9️⃣ List and Dict Validation

Make a model Patient with:

allergies: List[str]

contact_info: Dict[str, str]
Validate both and print them clearly.

"""

from pydantic import BaseModel
from typing import Dict,List

class Patient_veriables(BaseModel):
    allergies:List[str]
    contact:Dict[str,str]

def Patient(patient:Patient_veriables):
    print("Allergies:",patient.allergies)
    print("Contact:",patient.contact)

data = {'allergies':['Dust','Sunlight'],'contact':{'Mo_no':'1236547895','email_id':'abcd@gmail.com'}}
data_object = Patient_veriables(**data)
Patient(data_object)