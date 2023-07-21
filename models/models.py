from pydantic import BaseModel, EmailStr, validator
from typing import Dict
import re

def validate_brazilian_phone_number(phone_number: str) -> str:
    digits_only = "".join(filter(str.isdigit, phone_number))
    if len(digits_only) != 11:
        raise ValueError("Invalid Brazilian phone number format. Use '+55 (XX) XXXXX-XXXX'")
    return phone_number

def validate_brazilian_cep(cep: str) -> str:
    digits_only = "".join(filter(str.isdigit, cep))
    if len(digits_only) != 8:
        raise ValueError("Invalid Brazilian CEP format. Use 'XXXXXXXX'")
    return cep

class OrderBase(BaseModel):
    customer_name: str
    email: EmailStr
    cep: str 
    phone_number: str
    items: Dict[int, int]

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
    total: float
    id: int
    status: str

class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    @validator('price')
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be greater than zero")
        return value

    @validator('quantity')
    def validate_quantity(cls, value):
        if value < 0:
            raise ValueError("Quantity must be greater than zero")
        return value


