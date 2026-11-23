import allure

from scooter_api import assert_json_response, assert_ok


@allure.suite("Список заказов")
class TestOrderList:
    @allure.title("Тело ответа содержит список заказов")
    def test_list_orders_returns_list(self, api):
        body = assert_json_response(api.list_orders(), 200)
        orders = body["orders"]
        assert isinstance(orders, list)
        assert all(isinstance(order, dict) for order in orders)

    @allure.title("Список заказов курьера содержит принятый им заказ")
    def test_list_orders_for_courier(self, api, courier_id, created_order):
        assert_ok(api.accept_order(created_order["id"], courier_id))

        body = assert_json_response(api.list_orders(courier_id), 200)
        orders = body["orders"]
        assert isinstance(orders, list)
        assert any(order["id"] == created_order["id"] for order in orders)
