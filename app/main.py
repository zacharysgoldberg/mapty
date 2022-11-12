from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from models import User, Order
from routers import auth, orders
from routers.auth import hash_password
from routers import templates
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette import status
from datetime import datetime, date
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/src/static", StaticFiles(directory="src/static"), name="static")


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    user = User.find(User.username == "ExampleUser").all()
    # [If user does not exist create user and sample records for testing api]
    # if not user:
    #     user_model = User(
    #         username="ExampleUser",
    #         password=hash_password("test1234")
    #     )
    #     user_model.save()

    #     order_model1 = Order(
    #         order_date=date.today(),
    #         order_time=datetime.now(),
    #         address="6868 Capri Ave, Ventura CA",
    #     )
    #     order_model1.save()
    #     time.sleep(5)
    #     order_model2 = Order(
    #         order_date=date.today(),
    #         order_time=datetime.now(),
    #         address="311 E Daily Dr, Camarillo CA",
    #     )
    #     order_model2.save()
    #     time.sleep(5)
    #     order_model3 = Order(
    #         order_date=date.today(),
    #         order_time=datetime.now(),
    #         address="3900 Bluefin Cir, Oxnard CA",
    #     )
    #     order_model3.save()
    #     time.sleep(5)
    #     order_model4 = Order(
    #         order_date=date.today(),
    #         order_time=datetime.now(),
    #         address="2701 Saviers Rd, Oxnard CA"
    #     )
    #     order_model4.save()
    #     time.sleep(5)
    #     order_model5 = Order(
    #         order_date=date.today(),
    #         order_time=datetime.now(),
    #         address="4667 Telegraph Rd, Ventura CA"
    #     )
    #     order_model5.save()

    #     return templates.TemplateResponse('index.html', {'request': request})

    return RedirectResponse(url='/orders', status_code=status.HTTP_302_FOUND)


# [Connecting routers]
# app.include_router(auth.router)
app.include_router(orders.router)
