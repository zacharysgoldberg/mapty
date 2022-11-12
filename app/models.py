from datetime import datetime, date
from database import redis
from redis_om import Field, EmbeddedJsonModel, JsonModel, Migrator
from typing import Optional


class User(JsonModel):
    username: str = Field(index=True)
    password: str

    class Meta:
        database = redis


# class Address(EmbeddedJsonModel):
#     address_line_1: str
#     address_line_2: Optional[str]
#     city: str = Field(index=True)
#     state: str = Field(index=True)
#     postal_code: str = Field(index=True)


class Order(JsonModel):
    input_type: str
    order_date: str
    order_time: str
    address: Optional[str]
    coords: list = Field(index=True)
    status: str = Field(default='pending')  # pending, completed, refunded

    class Meta:
        database = redis


Migrator().run()
