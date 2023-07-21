import json
import os 
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from fastapi import FastAPI, HTTPException
from typing import Optional, List

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
    order_dict["status"] = "created"
    db_order = OrderDB(**order_dict)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    db.close()
    return order

@app.get("/orders/", response_model=List[OrderRead])
def read_order(order_id: Optional[int] = None):
    db = SessionLocal()

    if order_id is None:
        orders = db.query(OrderDB).all()
        db.close()
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found")
        
        order_list = []
        for order in orders:
            order_dict = order.__dict__
            order_dict["items"] = json.loads(order.items)
            order_list.append(OrderRead(**order_dict))

        return order_list
    
    else:
        order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
        db.close()
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        order_dict = order.__dict__
        order_dict["items"] = json.loads(order.items)

        return OrderRead(**order_dict)
