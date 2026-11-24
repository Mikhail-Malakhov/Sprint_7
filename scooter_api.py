import os

import allure

from data import (
    CONNECT_TIMEOUT,
    COURIER_LOGIN_PATH,
    COURIER_PATH,
    DEFAULT_API_URL,
    LONG_REQUEST_TIMEOUT,
    ORDER_ACCEPT_PATH,
    ORDER_CANCEL_PATH,
    ORDER_FINISH_PATH,
    ORDER_TRACK_PATH,
    ORDERS_PATH,
    REQUEST_TIMEOUT,
)


class ScooterApi:
    def __init__(self, session):
        self.session = session
        self.base_url = os.getenv("SCOOTER_API_URL", DEFAULT_API_URL).rstrip("/")

    def _request(self, method, path, *, payload=None, params=None, timeout=REQUEST_TIMEOUT):
        response = self.session.request(
            method,
            f"{self.base_url}{path}",
            json=payload,
            params=params,
            timeout=(CONNECT_TIMEOUT, timeout),
            allow_redirects=False,
        )
        allure.attach(str(response.status_code), "HTTP-статус", allure.attachment_type.TEXT)
        allure.attach(response.text, "Тело ответа", allure.attachment_type.TEXT)
        return response

    @allure.step("Отправить запрос на создание курьера: POST /courier")
    def create_courier(self, payload):
        return self._request("POST", COURIER_PATH, payload=payload)

    @allure.step("Отправить запрос на авторизацию курьера: POST /courier/login")
    def login_courier(self, credentials):
        # Пропущенный пароль может привести к ответу шлюза только через 60 секунд.
        timeout = REQUEST_TIMEOUT if "password" in credentials else LONG_REQUEST_TIMEOUT
        return self._request("POST", COURIER_LOGIN_PATH, payload=credentials, timeout=timeout)

    @allure.step("Отправить запрос на удаление курьера: DELETE /courier/{courier_id}")
    def delete_courier(self, courier_id=""):
        return self._request("DELETE", f"{COURIER_PATH}/{courier_id}")

    @allure.step("Отправить запрос на создание заказа: POST /orders")
    def create_order(self, payload):
        return self._request("POST", ORDERS_PATH, payload=payload)

    @allure.step("Отправить запрос на получение списка заказов: GET /orders")
    def list_orders(self, courier_id=None):
        params = {"limit": 1, "page": 0, "courierId": courier_id}
        return self._request("GET", ORDERS_PATH, params=params, timeout=LONG_REQUEST_TIMEOUT)

    @allure.step("Отправить запрос на получение заказа по трек-номеру: GET /orders/track")
    def track_order(self, track=None):
        return self._request("GET", ORDER_TRACK_PATH, params={"t": track})

    @allure.step("Отправить запрос на принятие заказа: PUT /orders/accept/{order_id}")
    def accept_order(self, order_id="", courier_id=None):
        return self._request(
            "PUT", f"{ORDER_ACCEPT_PATH}/{order_id}", params={"courierId": courier_id}
        )

    @allure.step("Отправить запрос на отмену заказа: PUT /orders/cancel")
    def cancel_order(self, track):
        return self._request("PUT", ORDER_CANCEL_PATH, params={"track": track})

    @allure.step("Отправить запрос на завершение заказа: PUT /orders/finish/{order_id}")
    def finish_order(self, order_id):
        return self._request("PUT", f"{ORDER_FINISH_PATH}/{order_id}")
