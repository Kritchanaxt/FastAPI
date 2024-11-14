
#? Normal operation

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Union

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str 
    price: float

@app.get("/hello")
def hello():
    return {"message": "Hello, World"}

@app.get("/items/{item_id}", response_model=dict)
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items_with_class", response_model=Item)
def create_item_with_class(item: Item):
    print(item.name, item.price)
    return item

@app.put("/items/{item_id}", response_model=Item)
def edit_item(item_id: int, item: Item):
    return item

@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}
