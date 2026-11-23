import os

import allure


DEFAULT_API_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
NONEXISTENT_ID = 2_147_483_647

COURIER_CREATE_MISSING_DATA = "Недостаточно данных для создания учетной записи"
COURIER_LOGIN_MISSING_DATA = "Недостаточно данных для входа"
COURIER_ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
ROUTE_NOT_FOUND = "Not Found."
COURIER_DELETE_NOT_FOUND = "Курьера с таким id нет."
ORDER_SEARCH_MISSING_DATA = "Недостаточно данных для поиска"
ORDER_TRACK_NOT_FOUND = "Заказ не найден"
ORDER_ID_NOT_FOUND = "Заказа с таким id не существует"
ORDER_COURIER_NOT_FOUND = "Курьера с таким id не существует"


class ScooterApi:
    def __init__(self, session):
        self.session = session
        self.base_url = os.getenv("SCOOTER_API_URL", DEFAULT_API_URL).rstrip("/")

    def _request(self, method, path, *, payload=None, params=None, timeout=25):
        with allure.step(f"{method} {path}"):
            response = self.session.request(
                method,
                f"{self.base_url}{path}",
                json=payload,
                params=params,
                timeout=(5, timeout),
                allow_redirects=False,
            )
            allure.attach(str(response.status_code), "HTTP-статус", allure.attachment_type.TEXT)
            return response

    def create_courier(self, payload):
        return self._request("POST", "/courier", payload=payload)

    def login_courier(self, credentials):
        # Пропущенный пароль может привести к ответу шлюза после 60 секунд.
        timeout = 75 if "password" not in credentials else 25
        return self._request("POST", "/courier/login", payload=credentials, timeout=timeout)

    def delete_courier(self, courier_id=None):
        path_id = "" if courier_id is None else str(courier_id)
        return self._request("DELETE", f"/courier/{path_id}")

    def create_order(self, payload):
        return self._request("POST", "/orders", payload=payload)

    def list_orders(self, courier_id=None):
        params = {"limit": 1, "page": 0, "courierId": courier_id}
        return self._request("GET", "/orders", params=params, timeout=75)

    def track_order(self, track=None):
        return self._request("GET", "/orders/track", params={"t": track})

    def accept_order(self, order_id=None, courier_id=None):
        path_id = "" if order_id is None else str(order_id)
        return self._request(
            "PUT", f"/orders/accept/{path_id}", params={"courierId": courier_id}
        )

    def cancel_order(self, track):
        return self._request("PUT", "/orders/cancel", params={"track": track})

    def finish_order(self, order_id):
        return self._request("PUT", f"/orders/finish/{order_id}")


def assert_json_response(response, expected_status):
    assert response.status_code == expected_status, (
        f"{response.request.method} {response.url}: ожидался {expected_status}, "
        f"получен {response.status_code}. Ответ: {response.text[:500]}"
    )
    assert "application/json" in response.headers.get("Content-Type", ""), (
        f"Сервер вернул ответ другого формата: {response.headers.get('Content-Type')}"
    )
    body = response.json()
    assert isinstance(body, dict), f"Ожидался JSON-объект, получено: {body!r}"
    return body


def assert_ok(response, expected_status=200):
    body = assert_json_response(response, expected_status)
    assert body == {"ok": True}
    assert body["ok"] is True


def assert_error(response, expected_status, message):
    body = assert_json_response(response, expected_status)
    assert body.get("message") == message, (
        f"Ожидалось сообщение {message!r}, получено {body.get('message')!r}"
    )
