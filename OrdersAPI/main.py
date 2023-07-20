import json

from fastapi import FastAPI, HTTPException

from db_models import OrderDB
from models import Order
from db import SessionLocal


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
