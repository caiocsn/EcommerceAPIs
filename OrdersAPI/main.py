import json
import os 
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from fastapi import FastAPI, HTTPException

from models.db_models import OrderDB
from models.models import OrderWrite, OrderRead
from db.db import SessionLocal
from .utils import call_subtract_items_api


app = FastAPI()

@app.post("/orders/", response_model=OrderWrite)
def create_order(order: OrderWrite):
    order_dict = order.dict()
    inventory_status = call_subtract_items_api(order_dict["items"])    
    if  inventory_status != 200:
        raise HTTPException(status_code = inventory_status , detail="Items not available")
    
    db = SessionLocal()
    order_dict["items"] = json.dumps(order_dict["items"])
    db_order = OrderDB(**order_dict)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    db.close()
    return order

@app.get("/orders/{order_id}", response_model=OrderRead)
def read_order(order_id: int):
    db = SessionLocal()
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    db.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_dict = order.__dict__
    order_dict["items"] = json.loads(order.items)

    return OrderRead(**order_dict)
