from typing import Optional
from fastapi import Request
from pydantic import BaseModel


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.pasword: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get('email')
        self.password = form.get('password')


class OrderBase(BaseModel):
    coords: list[float, float]
    date: str
    time: str
    _type: str


class Orders(BaseModel):
    orders: list[OrderBase] = ...
