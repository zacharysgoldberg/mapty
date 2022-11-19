from typing import Optional
from pydantic import BaseModel
# from datetime import datetime, date


class OrderBase(BaseModel):
    id: str
    inputType: str
    date: str
    time: str
    coords: list


class Orders(BaseModel):
    orders: list[OrderBase] = ...
