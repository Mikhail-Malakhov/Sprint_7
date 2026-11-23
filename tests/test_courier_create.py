from uuid import uuid4

import allure
import pytest

from scooter_api import COURIER_CREATE_MISSING_DATA, assert_error, assert_ok


@allure.suite("Создание курьера")
class TestCourierCreate:
    @allure.title("Курьер создаётся с указанным именем")
    def test_create_courier_returns_created(self, create_courier, courier_data):
        assert_ok(create_courier(courier_data), 201)

    @allure.title("Курьер создаётся без имени")
    def test_create_courier_without_first_name(self, create_courier, courier_data):
        courier_data.pop("firstName")
        assert_ok(create_courier(courier_data), 201)

    @allure.title("Для создания курьера обязательно поле {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field(
        self, create_courier, courier_data, missing_field
    ):
        courier_data.pop(missing_field)
        assert_error(create_courier(courier_data), 400, COURIER_CREATE_MISSING_DATA)

    @allure.title("Создание курьера с занятым логином ({case}) возвращает конфликт")
    @pytest.mark.parametrize("case", ["same_data", "different_data"])
    def test_create_courier_with_existing_login(self, create_courier, courier_data, case):
        assert_ok(create_courier(courier_data), 201)
        if case == "different_data":
            courier_data = {**courier_data, "password": uuid4().hex, "firstName": "Другой курьер"}
        response = create_courier(courier_data)
        assert_error(response, 409, "Этот логин уже используется. Попробуйте другой.")
