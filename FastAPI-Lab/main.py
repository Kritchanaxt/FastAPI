
#* Relational Database with SQLAlchemy in FastAPI 

from typing import Union, List

from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException

from .database import engine, Base, get_db
from .schema import ItemCreated, ItemResponse
from .models import Item


# Create Database
Base.metadata.create_all(bind=engine)


#? Step 4: Integrate with CRUD

app = FastAPI()

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreated, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())
    # db_item = Item(**item.dict())
    # db_item = Item(titles=item.title, description=item.description, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    return db_item

@app.get("/items", response_model=List[ItemResponse])
def read_item(db: Session = Depends(get_db)):
    db_item = db.query(Item).all()
    return db_item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreated, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)    
    db.commit()
    db.refresh(db_item)
    
    return db_item

# Delete: Delete products by ID.
@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}