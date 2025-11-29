import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str = "ali"
    number1: float
    number2: int

app = FastAPI()
database=[]

@app.get('/',response_model=Item)
def read_root():
    return {"name":"ali","number1":1.1,"number2":1}

@app.get('/items')
def read_items():
    return database

@app.post('/items')
def create_item(item: Item):
    database.append(item)
    print(item.name)
    return item

@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item):
    database[item_id] = item
    return item

@app.delete('/items/{item_id}')
def delete_item(item_id: int):
    del database[item_id]
    return {"message": "Item deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)