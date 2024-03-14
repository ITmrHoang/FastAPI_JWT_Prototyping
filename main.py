from typing import Union

from fastapi import FastAPI, Query, Path
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from core import constant

# load env in file .env
import os 
from dotenv import load_dotenv
# #Đặt đường dẫn cho tập tin .env
#dotenv_path = '/path/to/your/.env'
## Load biến môi trường từ tập tin .env tại đường dẫn tùy chỉnh
#load_dotenv(dotenv_path)
load_dotenv()
app = FastAPI()


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "Worlds1"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results