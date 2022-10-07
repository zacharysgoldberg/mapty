from fastapi import APIRouter, Request, Depends
from .auth import get_current_user
from models import Order
import requests
from commands.gps import get_coords_by_address, TSP, distances_from_coords
import csv
from . import templates
# import pandas as pd


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={401: {"order": "Not found"}}
)


@router.get('/')
async def order_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


# [Request to optimize path for orders/addresses]
@router.get('/optimize-path')
async def sort_order():
    # # [For CSV]
    # with open("api/routers/orders.csv", "r") as file:
    #     reader = csv.DictReader(file)
    #     # header = next(reader)
    #     addresses = [row['address'] for row in reader]

    # [For redis]
    pks = Order.all_pks()
    orders = [order for order in pks]
    addresses = [Order.get(pk).address for pk in orders]
    coords = [get_coords_by_address(order) for order in addresses]
    optimal_path = TSP(coords, 0)
    # order_of_path = [int(order) for order in orders]

    return {'orders': optimal_path}

# [Request to get the next order upon successful authorization]


@router.get('/get-next-order/{pk}')
async def get_next_order(request: Request, pk: str):
    # user = await get_current_user(request)
    # if user is None:
    #     response = requests.post("http://localhost:8000/auth/token",
    #                              data={"username": "ExampleUser", "password": "test1234!"})
    #     print(response.text)

    # [Returning next order based on order id]
    next_order = Order.get(pk)
    if next_order:
        print(next_order)
        return next_order

    return False

# [To update order delivery to True]


@router.post('/deliver-order/{pk}')
async def deliver_order(request: Request, pk: str):
    # user = await get_current_user(request)
    # if user is None:
    #     response = request.post("http://localhost:8000/auth/token",
    #                             data={"username": "ExampleUser", "password": "test1234!"})
    # print(response.text)

    order = Order.get(pk)
    order.status = 'completed'
    order.save()
    return True
