from uuid import uuid4

import allure
import pytest

from scooter_api import (
    COURIER_ACCOUNT_NOT_FOUND,
    COURIER_LOGIN_MISSING_DATA,
    assert_error,
    assert_json_response,
)


@allure.suite("Логин курьера")
class TestCourierLogin:
    @allure.title("Авторизация курьера возвращает его ID")
    def test_login_returns_courier_id(self, api, registered_courier):
        body = assert_json_response(api.login_courier(registered_courier), 200)
        assert type(body["id"]) is int and body["id"] > 0

    @allure.title("Для авторизации курьера обязательно поле {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_without_required_field(self, api, registered_courier, missing_field):
        credentials = registered_courier.copy()
        credentials.pop(missing_field)
        assert_error(api.login_courier(credentials), 400, COURIER_LOGIN_MISSING_DATA)

    @allure.title("Авторизация с неверным полем {invalid_field} возвращает ошибку")
    @pytest.mark.parametrize("invalid_field", ["login", "password"])
    def test_login_with_incorrect_credentials(self, api, registered_courier, invalid_field):
        credentials = {**registered_courier, invalid_field: f"invalid_{uuid4().hex}"}
        assert_error(api.login_courier(credentials), 404, COURIER_ACCOUNT_NOT_FOUND)

    @allure.title("Несуществующий курьер не может авторизоваться")
    def test_login_with_unregistered_courier(self, api, courier_data):
        credentials = {key: courier_data[key] for key in ("login", "password")}
        assert_error(api.login_courier(credentials), 404, COURIER_ACCOUNT_NOT_FOUND)
