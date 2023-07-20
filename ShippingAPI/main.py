import os 
import sys
import json

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from fastapi import FastAPI, HTTPException

from models.models import OrderRead
from models.db_models import OrderDB
from db.db import SessionLocal

app = FastAPI()

@app.post("/shipping/processing/{order_id}")
def confirm_payment(order_id: int):
    db = SessionLocal()
    db_order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    
    if not db_order:
        db.close()
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.status != "payed":
        db.close()
        raise HTTPException(status_code=400, detail="Invalid status change")
    
    db_order.status = "processing"    
    db.commit()
    db.refresh(db_order)
    db.close()

    order_dict = db_order.__dict__
    order_dict["items"] = json.loads(db_order.items)
    return OrderRead(**order_dict)

@app.post("/shipping/sent/{order_id}")
def confirm_payment(order_id: int):
    db = SessionLocal()
    db_order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    
    if not db_order:
        db.close()
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.status not in ['processing', 'payed']:
        db.close()
        raise HTTPException(status_code=400, detail="Invalid status change")
    
    db_order.status = "sent"    
    db.commit()
    db.refresh(db_order)
    db.close()

    order_dict = db_order.__dict__
    order_dict["items"] = json.loads(db_order.items)
    return OrderRead(**order_dict)


@app.post("/shipping/delivered/{order_id}")
def confirm_payment(order_id: int):
    db = SessionLocal()
    db_order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    
    if not db_order:
        db.close()
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.status not in ['processing', 'payed', 'sent']:
        db.close()
        raise HTTPException(status_code=400, detail="Invalid status change")
    
    db_order.status = "delivered"    
    db.commit()
    db.refresh(db_order)
    db.close()

    order_dict = db_order.__dict__
    order_dict["items"] = json.loads(db_order.items)
    return OrderRead(**order_dict)