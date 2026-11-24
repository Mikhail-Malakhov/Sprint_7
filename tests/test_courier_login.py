import allure
import pytest

from data import COURIER_ACCOUNT_NOT_FOUND, COURIER_LOGIN_MISSING_DATA, INVALID_VALUE_PREFIX
from helpers import generate_random_string, get_credentials


@allure.suite("Логин курьера")
class TestCourierLogin:
    @allure.title("Авторизация курьера возвращает его ID")
    def test_login_returns_courier_id(self, api, registered_courier):
        with allure.step("Авторизоваться под зарегистрированным курьером"):
            response = api.login_courier(get_credentials(registered_courier))
        with allure.step("Проверить код 200 и ID курьера в ответе"):
            assert response.status_code == 200
            assert response.json()["id"] == registered_courier["id"]

    @allure.title("Для авторизации курьера обязательно поле {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_without_required_field(self, api, registered_courier, missing_field):
        with allure.step(f"Подготовить данные для входа без поля {missing_field}"):
            credentials = get_credentials(registered_courier)
            credentials.pop(missing_field)
        with allure.step("Авторизоваться"):
            response = api.login_courier(credentials)
        with allure.step("Проверить код 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["message"] == COURIER_LOGIN_MISSING_DATA

    @allure.title("Авторизация с неверным полем {invalid_field} возвращает ошибку")
    @pytest.mark.parametrize("invalid_field", ["login", "password"])
    def test_login_with_incorrect_credentials(self, api, registered_courier, invalid_field):
        with allure.step(f"Подготовить данные для входа с неверным полем {invalid_field}"):
            credentials = {
                **get_credentials(registered_courier),
                invalid_field: generate_random_string(INVALID_VALUE_PREFIX),
            }
        with allure.step("Авторизоваться"):
            response = api.login_courier(credentials)
        with allure.step("Проверить код 404 и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == COURIER_ACCOUNT_NOT_FOUND

    @allure.title("Несуществующий курьер не может авторизоваться")
    def test_login_with_unregistered_courier(self, api, courier_data):
        with allure.step("Авторизоваться под незарегистрированным курьером"):
            response = api.login_courier(get_credentials(courier_data))
        with allure.step("Проверить код 404 и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == COURIER_ACCOUNT_NOT_FOUND
