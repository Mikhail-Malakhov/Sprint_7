import allure

from scooter_api import (
    NONEXISTENT_ID,
    ORDER_COURIER_NOT_FOUND,
    ORDER_ID_NOT_FOUND,
    ORDER_SEARCH_MISSING_DATA,
    ROUTE_NOT_FOUND,
    assert_error,
    assert_ok,
)


@allure.suite("Принятие заказа")
class TestOrderAccept:
    @allure.title("Курьер принимает заказ")
    def test_accept_order(self, api, courier_id, created_order):
        assert_ok(api.accept_order(created_order["id"], courier_id))

    @allure.title("Принятие заказа без ID курьера возвращает ошибку")
    def test_accept_order_without_courier_id(self, api, created_order):
        response = api.accept_order(order_id=created_order["id"])
        assert_error(response, 400, ORDER_SEARCH_MISSING_DATA)

    @allure.title("Несуществующий курьер не может принять заказ")
    def test_accept_order_with_nonexistent_courier(self, api, created_order):
        response = api.accept_order(created_order["id"], NONEXISTENT_ID)
        assert_error(response, 404, ORDER_COURIER_NOT_FOUND)

    @allure.title("Принятие заказа без ID заказа возвращает ошибку")
    def test_accept_order_without_order_id(self, api, courier_id):
        response = api.accept_order(courier_id=courier_id)
        assert_error(response, 404, ROUTE_NOT_FOUND)

    @allure.title("Курьер не может принять несуществующий заказ")
    def test_accept_nonexistent_order(self, api, courier_id):
        response = api.accept_order(NONEXISTENT_ID, courier_id)
        assert_error(response, 404, ORDER_ID_NOT_FOUND)
