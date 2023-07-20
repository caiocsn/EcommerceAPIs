from fastapi import FastAPI, HTTPException, Query

from models import Item
from db_models import ItemDB
from db import SessionLocal
from typing import List, Optional

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
    return Item(**item.__dict__)
