import allure

from data import (
    NONEXISTENT_ID,
    OK_RESPONSE,
    ORDER_COURIER_NOT_FOUND,
    ORDER_ID_NOT_FOUND,
    ORDER_SEARCH_MISSING_DATA,
    ROUTE_NOT_FOUND,
)


@allure.suite("Принятие заказа")
class TestOrderAccept:
    @allure.title("Курьер принимает заказ")
    def test_accept_order(self, api, registered_courier, created_order):
        with allure.step("Принять заказ курьером"):
            response = api.accept_order(created_order["id"], registered_courier["id"])
        with allure.step("Проверить код 200 и тело ответа ok: true"):
            assert response.status_code == 200
            assert response.json() == OK_RESPONSE

    @allure.title("Принятие заказа без ID курьера возвращает ошибку")
    def test_accept_order_without_courier_id(self, api, created_order):
        with allure.step("Принять заказ без ID курьера"):
            response = api.accept_order(order_id=created_order["id"])
        with allure.step("Проверить код 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["message"] == ORDER_SEARCH_MISSING_DATA

    @allure.title("Несуществующий курьер не может принять заказ")
    def test_accept_order_with_nonexistent_courier(self, api, created_order):
        with allure.step("Принять заказ несуществующим курьером"):
            response = api.accept_order(created_order["id"], NONEXISTENT_ID)
        with allure.step("Проверить код 404 и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == ORDER_COURIER_NOT_FOUND

    @allure.title("Принятие заказа без ID заказа возвращает ошибку")
    def test_accept_order_without_order_id(self, api, registered_courier):
        with allure.step("Принять заказ без ID заказа"):
            response = api.accept_order(courier_id=registered_courier["id"])
        with allure.step("Проверить код 404 и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == ROUTE_NOT_FOUND

    @allure.title("Курьер не может принять несуществующий заказ")
    def test_accept_nonexistent_order(self, api, registered_courier):
        with allure.step("Принять несуществующий заказ"):
            response = api.accept_order(NONEXISTENT_ID, registered_courier["id"])
        with allure.step("Проверить код 404 и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == ORDER_ID_NOT_FOUND
