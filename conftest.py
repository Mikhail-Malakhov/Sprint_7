import pytest
import requests

from helpers import (
    delete_courier_by_credentials,
    delete_order,
    delete_order_from_response,
    generate_courier_data,
    generate_order_data,
    get_credentials,
)
from scooter_api import ScooterApi


@pytest.fixture
def api():
    with requests.Session() as session:
        yield ScooterApi(session)


@pytest.fixture
def courier_data(api):
    """Данные нового курьера. Курьер создаётся в тесте, удаляется здесь после теста."""
    data = generate_courier_data()
    credentials = get_credentials(data)
    yield data
    delete_courier_by_credentials(api, credentials)


@pytest.fixture
def registered_courier(api):
    """Создаёт курьера перед тестом и удаляет его после теста."""
    data = generate_courier_data()
    credentials = get_credentials(data)
    api.create_courier(data)
    courier_id = api.login_courier(credentials).json()["id"]
    yield {**credentials, "id": courier_id}
    delete_courier_by_credentials(api, credentials)


@pytest.fixture
def order_data():
    return generate_order_data()


@pytest.fixture
def create_order(api):
    """Создаёт заказы в тесте и отменяет их после теста."""
    responses = []

    def create(payload):
        response = api.create_order(payload)
        responses.append(response)
        return response

    yield create
    for response in responses:
        delete_order_from_response(api, response)


@pytest.fixture
def created_order(api):
    """Создаёт заказ перед тестом и отменяет его после теста."""
    track = api.create_order(generate_order_data()).json()["track"]
    order = api.track_order(track).json()["order"]
    yield order
    delete_order(api, track)
