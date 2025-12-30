"""
#Nested Models in Pydantic

->Nested Models are used to represent complex or structured data inside another model.
->For example, if a user has an address containing fields like city, state, and pincode, we can create a separate Address model and include it inside the main User model.
->This makes the data organized, reusable, and easy to access.
->Nested models help handle JSON or dictionary data that contain multiple layers or sub-objects.

In short:
Nested Models = Models inside models → used to manage and validate structured or hierarchical data
"""
from pydantic import BaseModel

class Address(BaseModel):
    city:str
    country:str
    pincode:int

class Patient(BaseModel):
    name:str
    age:int
    gender:str
    address:Address

def demo(patient:Patient):
    print("Name:",patient.name)
    print("Pincode:",patient.address.pincode) 
#create a Dict for Adress
Address_dict = {'city': 'Bhavnagar','country': 'India','pincode': 123654}

#Create a Object for Dict.
address1 = Address(**Address_dict)

#Make Dict for Patient Data
Patient_dict = {'name': 'Ravi','age': 60,'gender': 'Male','address':address1}

#Make a Object for Patient.
patient1 = Patient(**Patient_dict)
demo(patient1)

# temp = patient1.model_dump()
# print(temp)
# print(type(temp))
# temp2 = patient1.model_dump_json()
# print(temp2)
# print(type(temp2))

# print("Name:",patient1.name)
# print("Age:",patient1.age)
# print("Gender:",patient1.gender)
# print("City Name:",patient1.address.city)
# print("Country Name:",patient1.address.country)
# print("Pincode :",patient1.address.pincode)