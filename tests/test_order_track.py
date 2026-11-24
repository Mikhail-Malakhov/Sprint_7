import allure

from data import NONEXISTENT_ID, ORDER_SEARCH_MISSING_DATA, ORDER_TRACK_NOT_FOUND


@allure.suite("Получение заказа по трек-номеру")
class TestOrderTrack:
    @allure.title("По трек-номеру возвращается объект созданного заказа")
    def test_track_order_returns_order(self, api, created_order):
        with allure.step("Получить заказ по трек-номеру"):
            response = api.track_order(created_order["track"])
        with allure.step("Проверить код 200 и данные заказа в ответе"):
            assert response.status_code == 200
            order = response.json()["order"]
            assert order["track"] == created_order["track"]
            assert order["id"] == created_order["id"]

    @allure.title("Поиск без трек-номера возвращает ошибку")
    def test_track_order_without_number(self, api):
        with allure.step("Получить заказ без трек-номера"):
            response = api.track_order()
        with allure.step("Проверить код 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["message"] == ORDER_SEARCH_MISSING_DATA

    @allure.title("Поиск по несуществующему трек-номеру возвращает ошибку")
    def test_track_order_with_nonexistent_number(self, api):
        with allure.step("Получить заказ по несуществующему трек-номеру"):
            response = api.track_order(NONEXISTENT_ID)
        with allure.step("Проверить код 404 и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == ORDER_TRACK_NOT_FOUND
