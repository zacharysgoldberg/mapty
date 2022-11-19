from . import client
import json


def test_optimize_path():
    response = client.get('/orders')

    assert type(json.loads(response.text)) is dict
    # assert type(json.loads(response.text)['orders']) is list


def test_get_next_order():
    order_id = 1
    access_token = client.post(
        '/auth/token', data={"username": "ExampleUser", "password": "test1234!"})
    response = client.get(
        f'/orders/get-next-order/{order_id}', cookies=access_token.cookies)

    assert json.loads(response.text)['address'] != 'false'
