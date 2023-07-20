from pydantic import BaseModel, EmailStr, validator
from typing import List
import re

def validate_brazilian_phone_number(phone_number: str) -> str:
    digits_only = "".join(filter(str.isdigit, phone_number))
    if len(digits_only) != 11:
        raise ValueError("Invalid Brazilian phone number format. Use '+55 (XX) XXXXX-XXXX'")
    return phone_number

def validate_brazilian_cep(cep: str) -> str:
    # Brazilian CEP pattern: 5 digits, followed by a dash, and 3 more digits
    pattern = r"^\d{5}-\d{3}$"
    if not re.match(pattern, cep):
        raise ValueError("Invalid Brazilian CEP format. Use 'XXXXX-XXX'")
    return cep

class OrderBase(BaseModel):
    customer_name: str
    email: EmailStr
    cep: str 
    phone_number: str
    items: List[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        exclude = {"id"}

    @validator("items")
    def validate_items(cls, v):
        if not v:
            raise ValueError("must provide at least one item")
        return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        return validate_brazilian_phone_number(v)
    
    @validator("cep")
    def validate_cep(cls, v):
        return validate_brazilian_cep(v)
    
class OrderWrite(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int