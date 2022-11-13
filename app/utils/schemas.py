from typing import Optional
from fastapi import Request
from pydantic import BaseModel
# from datetime import datetime, date


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
    inputType: str
    date: str
    time: str
    coords: list


class Orders(BaseModel):
    orders: list[OrderBase] = ...
