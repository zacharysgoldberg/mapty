from . import client


def test_create_user():
    response = client.get('/')

    assert response.status_code == 200
    assert response.text.strip('\"') == "Pizza Drone"


def test_auth():
    response = client.post(
        '/auth/token', data={"username": "ExampleUser", "password": "test1234!"})

    assert response.text.strip('\"') == 'true'
    assert response.cookies is not None
