import allure
import pytest

from data import (
    ANOTHER_COURIER_FIRST_NAME,
    COURIER_CREATE_MISSING_DATA,
    COURIER_LOGIN_ALREADY_USED,
    OK_RESPONSE,
)
from helpers import generate_random_string


@allure.suite("Создание курьера")
class TestCourierCreate:
    @allure.title("Курьер создаётся с указанным именем")
    def test_create_courier_returns_created(self, api, courier_data):
        with allure.step("Создать курьера с логином, паролем и именем"):
            response = api.create_courier(courier_data)
        with allure.step("Проверить код 201 и тело ответа ok: true"):
            assert response.status_code == 201
            assert response.json() == OK_RESPONSE

    @allure.title("Курьер создаётся без имени")
    def test_create_courier_without_first_name(self, api, courier_data):
        with allure.step("Подготовить данные курьера без имени"):
            payload = {"login": courier_data["login"], "password": courier_data["password"]}
        with allure.step("Создать курьера"):
            response = api.create_courier(payload)
        with allure.step("Проверить код 201 и тело ответа ok: true"):
            assert response.status_code == 201
            assert response.json() == OK_RESPONSE

    @allure.title("Для создания курьера обязательно поле {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field(self, api, courier_data, missing_field):
        with allure.step(f"Подготовить данные курьера без поля {missing_field}"):
            payload = courier_data.copy()
            payload.pop(missing_field)
        with allure.step("Создать курьера"):
            response = api.create_courier(payload)
        with allure.step("Проверить код 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["message"] == COURIER_CREATE_MISSING_DATA

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_courier_with_same_data_returns_conflict(self, api, courier_data):
        with allure.step("Создать курьера"):
            first_response = api.create_courier(courier_data)
        with allure.step("Повторно создать курьера с теми же данными"):
            response = api.create_courier(courier_data)
        with allure.step("Проверить, что первый курьер создан, а второй получил код 409"):
            assert first_response.json() == OK_RESPONSE
            assert response.status_code == 409
            assert response.json()["message"] == COURIER_LOGIN_ALREADY_USED

    @allure.title("Нельзя создать курьера с уже занятым логином")
    def test_create_courier_with_existing_login_returns_conflict(self, api, courier_data):
        with allure.step("Создать курьера"):
            first_response = api.create_courier(courier_data)
        with allure.step("Подготовить данные с тем же логином, другим паролем и именем"):
            payload = {
                **courier_data,
                "password": generate_random_string(),
                "firstName": ANOTHER_COURIER_FIRST_NAME,
            }
        with allure.step("Создать курьера с занятым логином"):
            response = api.create_courier(payload)
        with allure.step("Проверить, что первый курьер создан, а второй получил код 409"):
            assert first_response.json() == OK_RESPONSE
            assert response.status_code == 409
            assert response.json()["message"] == COURIER_LOGIN_ALREADY_USED
