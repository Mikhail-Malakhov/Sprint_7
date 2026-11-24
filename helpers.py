from datetime import date, timedelta
from uuid import uuid4

import allure
import requests

from data import (
    COURIER_FIRST_NAME,
    COURIER_LOGIN_PREFIX,
    GATEWAY_ERROR_CODES,
    ORDER_COMMENT_PREFIX,
    ORDER_DATA,
    ORDER_DELIVERY_DAYS,
)


def generate_random_string(prefix=""):
    return f"{prefix}{uuid4().hex}"


def generate_courier_data():
    return {
        "login": generate_random_string(COURIER_LOGIN_PREFIX),
        "password": generate_random_string(),
        "firstName": COURIER_FIRST_NAME,
    }


def get_credentials(courier):
    return {"login": courier["login"], "password": courier["password"]}


def generate_order_data():
    delivery_date = date.today() + timedelta(days=ORDER_DELIVERY_DAYS)
    return {
        **ORDER_DATA,
        "deliveryDate": delivery_date.isoformat(),
        "comment": generate_random_string(ORDER_COMMENT_PREFIX),
    }


def retry_on_gateway_error(operation, *args):
    try:
        response = operation(*args)
    except (requests.Timeout, requests.ConnectionError):
        return operation(*args)
    if response.status_code in GATEWAY_ERROR_CODES:
        return operation(*args)
    return response


@allure.step("Удалить тестового курьера, если он был создан")
def delete_courier_by_credentials(api, credentials):
    login = retry_on_gateway_error(api.login_courier, credentials)
    if login.status_code != 200:
        return
    retry_on_gateway_error(api.delete_courier, login.json()["id"])


@allure.step("Отменить или завершить тестовый заказ {track}")
def delete_order(api, track):
    cancel = retry_on_gateway_error(api.cancel_order, track)
    if cancel.status_code != 409:
        return
    tracked = retry_on_gateway_error(api.track_order, track)
    if tracked.status_code != 200:
        return
    order = tracked.json()["order"]
    if order["finished"] or order["cancelled"]:
        return
    retry_on_gateway_error(api.finish_order, order["id"])


def delete_order_from_response(api, response):
    if response.status_code != 201:
        return
    delete_order(api, response.json()["track"])
