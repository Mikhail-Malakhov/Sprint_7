import allure

from data import OK_RESPONSE


@allure.suite("Список заказов")
class TestOrderList:
    @allure.title("Тело ответа содержит список заказов")
    def test_list_orders_returns_list(self, api):
        with allure.step("Получить список заказов"):
            response = api.list_orders()
        with allure.step("Проверить код 200 и список заказов в ответе"):
            assert response.status_code == 200
            assert isinstance(response.json()["orders"], list)

    @allure.title("Список заказов курьера содержит принятый им заказ")
    def test_list_orders_for_courier(self, api, registered_courier, created_order):
        with allure.step("Принять заказ курьером"):
            accept_response = api.accept_order(created_order["id"], registered_courier["id"])
        with allure.step("Получить список заказов курьера"):
            response = api.list_orders(registered_courier["id"])
        with allure.step("Проверить, что принятый заказ есть в списке курьера"):
            assert accept_response.json() == OK_RESPONSE
            assert response.status_code == 200
            order_ids = [order["id"] for order in response.json()["orders"]]
            assert created_order["id"] in order_ids
