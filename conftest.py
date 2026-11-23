from datetime import date, timedelta
from uuid import uuid4

import allure
import pytest
import requests

from scooter_api import (
    COURIER_ACCOUNT_NOT_FOUND,
    COURIER_DELETE_NOT_FOUND,
    ScooterApi,
    assert_error,
    assert_json_response,
    assert_ok,
)


@pytest.fixture
def api():
    with requests.Session() as session:
        yield ScooterApi(session)


@pytest.fixture
def courier_data():
    return {
        "login": f"sprint7_{uuid4().hex}",
        "password": uuid4().hex,
        "firstName": "Тестовый курьер",
    }


def retry_cleanup(operation, *args):
    try:
        response = operation(*args)
    except (requests.Timeout, requests.ConnectionError):
        return operation(*args)
    if response.status_code in (502, 503, 504):
        return operation(*args)
    return response


@pytest.fixture
def create_courier(api, request):
    def create(payload):
        if {"login", "password"} <= payload.keys():
            credentials = {key: payload[key] for key in ("login", "password")}
            request.addfinalizer(lambda: clear_courier(credentials))
        return api.create_courier(payload)

    def clear_courier(credentials):
        with allure.step("Удалить тестового курьера"):
            login = retry_cleanup(api.login_courier, credentials)
            if login.status_code == 404:
                assert_error(login, 404, COURIER_ACCOUNT_NOT_FOUND)
                return
            courier_id = assert_json_response(login, 200)["id"]
            delete = retry_cleanup(api.delete_courier, courier_id)
            if delete.status_code == 404:
                assert_error(delete, 404, COURIER_DELETE_NOT_FOUND)
            else:
                assert_ok(delete)

    return create


@pytest.fixture
def registered_courier(create_courier, courier_data):
    with allure.step("Зарегистрировать тестового курьера"):
        assert_ok(create_courier(courier_data), 201)
    return {key: courier_data[key] for key in ("login", "password")}


@pytest.fixture
def courier_id(api, registered_courier):
    response = api.login_courier(registered_courier)
    courier_id = assert_json_response(response, 200)["id"]
    assert type(courier_id) is int and courier_id > 0
    return courier_id


@pytest.fixture
def order_data():
    return {
        "firstName": "Тестовый",
        "lastName": "Заказ",
        "address": "Тестовая улица, 1",
        "metroStation": "4",
        "phone": "+70000000000",
        "rentTime": 1,
        "deliveryDate": (date.today() + timedelta(days=2)).isoformat(),
        "comment": f"Sprint 7: {uuid4().hex}",
    }


@pytest.fixture
def create_order(api, request):
    def create(payload):
        response = api.create_order(payload)
        if response.ok:
            track = response.json().get("track")
            if type(track) is int and track > 0:
                request.addfinalizer(lambda: clear_order(track))
        return response

    def clear_order(track):
        with allure.step(f"Очистить тестовый заказ с трек-номером {track}"):
            result = retry_cleanup(api.cancel_order, track)
            if result.status_code == 409:
                order = assert_json_response(retry_cleanup(api.track_order, track), 200)["order"]
                assert order["track"] == track
                if order["finished"] or order["cancelled"]:
                    return
                completed = retry_cleanup(api.finish_order, order["id"])
                if completed.status_code == 409:
                    order = assert_json_response(retry_cleanup(api.track_order, track), 200)["order"]
                    assert order["track"] == track and order["finished"] is True
                else:
                    assert_ok(completed)
            else:
                assert_ok(result)

    return create


@pytest.fixture
def created_order_track(create_order, order_data):
    with allure.step("Создать тестовый заказ"):
        response = create_order(order_data)
        track = assert_json_response(response, 201)["track"]
        assert type(track) is int and track > 0
    return track


@pytest.fixture
def created_order(api, created_order_track):
    order = assert_json_response(api.track_order(created_order_track), 200)["order"]
    assert order["track"] == created_order_track
    return order
