from datetime import datetime
from typing import Optional
from pydantic import BaseModel
# from datetime import datetime, date


class LocationBase(BaseModel):
    id: str
    inputType: str
    date: str
    time: datetime
    coords: list


class Locations(BaseModel):
    orders: list[LocationBase] = ...
