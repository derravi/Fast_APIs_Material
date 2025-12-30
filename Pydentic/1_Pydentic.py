# Pydantic Overview

# In Python, type validation is not built-in at the runtime level.
# Let's understand this with examples.

# Example 1: No Type Validation in Normal Functions

def add(name, age):
    print(name)
    print(age)
    print("Data Added.")

add("ravi", "Five")  # 'age' is not int, but Python does not raise an error

# Here, we see Python does not enforce type validation automatically.

# Example 2: Manual Type Checking (Not Practical)

def update(name: str, age: int):
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print("Updated")
    else:
        raise TypeError("Check the type of the given parameters.")

update("Ravi", 5)

# Even with manual type checks, this approach is not scalable for large data sets or databases.

# Why We Need Pydantic
# Pydantic provides automatic data validation and type enforcement using Python type hints.
# You define a model that describes what your data should look like, and Pydantic validates the input automatically.

# Steps of Pydantic Validation
# 1. Define a Pydantic model
#    Create a class that defines your expected fields, types, and validation constraints.

# 2. Instantiate the model with raw data
#    When you pass data (e.g., a dictionary), Pydantic validates it automatically, converts compatible types,
#    and raises ValidationError if invalid.

# 3. Use the validated model safely
#    Once validated, you can pass the model around with confidence that it’s type-safe.

# Additional Notes
# - Optional → Used when a field can be None or missing.
# - EmailStr → Used to validate email syntax automatically.
# - AnyUrl → Used to validate a URL field.
# - Field() → Used to set constraints (like max_length, gt, lt, default, etc.).
# - Annotated → Adds metadata or validation details for a type hint.
#   Useful in Pydantic v2 or FastAPI for attaching rules and documentation.


from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional


# Define a Pydantic model
class VariableTesting(BaseModel):
    name: str = Field(
        max_length=50,
        title="Name of the Patient",
        description="Enter the name of the patient.",
        examples=["Ravi", "Nikul"]
    )
    age: int = Field(gt=18, description="Age must be greater than 18.")
    email: EmailStr = Field(max_length=30, description="Enter a valid email address.")
    mo_no: str = Field(max_length=10, description="Enter a valid 10-digit mobile number.")
    linkedin_profile: Optional[AnyUrl] = Field(
        max_length=200, description="Enter a valid LinkedIn profile URL."
    )
    weight: Optional[float] = Field(
        le=120, description="Enter weight (should not exceed 120 kg)."
    )
    married: Optional[bool] = Field(
        default=None,
        title="Marital Status",
        description="Enter marital status as True/False or 1/0."
    )
    allergies: Optional[List[str]] = Field(
        max_length=4, description="List of allergies (up to 4 items)."
    )
    contact_details: Dict[str, str] = Field(
        description="Dictionary containing patient contact details (e.g., phone, address)."
    )


# Function to print patient details
def patient_info(patient: VariableTesting):
    print("\n--- Patient Information ---")
    print("Name:", patient.name)
    print("Age:", patient.age)
    print("Mobile No:", patient.mo_no)
    print("Email:", patient.email)
    print("LinkedIn Profile:", patient.linkedin_profile)
    print("Weight:", patient.weight)
    print("Married:", patient.married)
    print("Allergies:", patient.allergies)
    print("Contact Details:", patient.contact_details)
    print("\nPatient data validated successfully!")


# Example input data
data = {
    'name': "Ravi",
    'age': 80,
    'email': 'ravider98@gmail.com',
    'married': True,
    'mo_no': '9966554321',
    'linkedin_profile': 'https://www.linkedin.com',
    'weight': 81.23,
    'allergies': ['Dust', 'Sunlight'],
    'contact_details': {'number': '1234567891', 'address': 'Surat'}
}

# Validate and print
patient = VariableTesting(**data)
patient_info(patient)