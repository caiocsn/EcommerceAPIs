import json
import re

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator
from typing import List

from db_models import *
from db import SessionLocal

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

class Order(BaseModel):
    customer_name: str
    email: EmailStr
    cep: str 
    phone_number: str
    items: List[str]

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

app = FastAPI()

@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    db = SessionLocal()
    order_dict = order.dict()
    order_dict["items"] = json.dumps(order_dict["items"])
    db_order = OrderDB(**order_dict)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    db.close()
    return order

@app.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int):
    db = SessionLocal()
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    db.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_dict = order.__dict__
    order_dict["items"] = json.loads(order.items)

    return Order(**order_dict)
