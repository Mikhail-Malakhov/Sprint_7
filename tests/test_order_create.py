import allure
import pytest

from data import ORDER_COLORS


@allure.suite("Создание заказа")
class TestOrderCreate:
    @allure.title("Создание заказа с цветом {color_name} возвращает трек-номер")
    @pytest.mark.parametrize("color_name", list(ORDER_COLORS))
    def test_create_order_with_color_returns_track(self, create_order, order_data, color_name):
        with allure.step(f"Создать заказ с цветом {color_name}"):
            response = create_order({**order_data, "color": ORDER_COLORS[color_name]})
        with allure.step("Проверить код 201 и трек-номер в ответе"):
            assert response.status_code == 201
            track = response.json()["track"]
            assert type(track) is int and track > 0

    @allure.title("Создание заказа без цвета возвращает трек-номер")
    def test_create_order_without_color_returns_track(self, create_order, order_data):
        with allure.step("Создать заказ без поля color"):
            response = create_order(order_data)
        with allure.step("Проверить код 201 и трек-номер в ответе"):
            assert response.status_code == 201
            track = response.json()["track"]
            assert type(track) is int and track > 0
