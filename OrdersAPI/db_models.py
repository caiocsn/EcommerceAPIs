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