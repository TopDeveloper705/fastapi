from fastapi import Body, FastAPI, Path, Query
from starlette.status import HTTP_201_CREATED
from pydantic import BaseModel
from pydantic.types import UrlStr
from typing import Set, List

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: Set[str] = []


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(*, item: Item):
    return item
