from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean

Base = declarative_base()

class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String, index=True)
    email = Column(String)
    cep = Column(String)
    phone_number = Column(String)
    items = Column(Text)


'''# order_management.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, constr, validator
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic, PydanticModel

DATABASE_URL = "sqlite:///./orders.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Order(BaseModel, PydanticModel):
    id: int
    customer_name: str
    email: EmailStr
    cep: str 
    phone_number: str
    items: List[str]

    class Config:
        orm_mode = True

# ... (rest of the code)
'''

