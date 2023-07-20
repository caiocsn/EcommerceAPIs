import os 
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from fastapi import FastAPI, HTTPException, Query

from typing import List, Optional, Dict

from models.models import Item
from models.db_models import ItemDB
from db.db import SessionLocal

app = FastAPI()

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    db = SessionLocal()
    db_item = ItemDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return Item(**db_item.__dict__)

@app.get("/items/", response_model=List[Item])
def read_items(item_ids: Optional[List[int]] = Query(None)):
    db = SessionLocal()
    if item_ids is None:
        items = db.query(ItemDB).all()
    else:
        items = db.query(ItemDB).filter(ItemDB.id.in_(item_ids)).all()
    db.close()
    if not items:
        raise HTTPException(status_code=404, detail="Items not found")

    return [Item(**item.__dict__) for item in items]


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    db = SessionLocal()
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    db.close()
    return Item(**db_item.__dict__)

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    db = SessionLocal()
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    db.close()
    return Item(**  item.__dict__)

@app.put("/items/subtract/")
def subtract_items(items_to_subtract: Dict[int, int]):
    db = SessionLocal()

    for item_id, quantity_to_subtract in items_to_subtract.items():
        item = db.query(ItemDB).filter(ItemDB.id == item_id).first()

        if quantity_to_subtract <= 0:
            db.close()
            raise HTTPException(status_code=400, detail=f"Invalid quantity to subtract for item with id {item_id}")

        if item is None:
            db.close()
            raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")

        if item.quantity < quantity_to_subtract:
            db.close()
            raise HTTPException(status_code=400, detail=f"Not enough items of id {item_id} in the inventory")

        item.quantity -= quantity_to_subtract

    db.commit()
    db.close()

    return {"message": "Items subtracted successfully"}