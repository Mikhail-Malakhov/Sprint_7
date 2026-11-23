import allure

from scooter_api import (
    NONEXISTENT_ID,
    ORDER_SEARCH_MISSING_DATA,
    ORDER_TRACK_NOT_FOUND,
    assert_error,
    assert_json_response,
)


@allure.suite("Получение заказа по трек-номеру")
class TestOrderTrack:
    @allure.title("По трек-номеру возвращается объект созданного заказа")
    def test_track_order_returns_order(self, api, created_order_track):
        body = assert_json_response(api.track_order(created_order_track), 200)
        order = body["order"]
        assert isinstance(order, dict)
        assert order["track"] == created_order_track
        assert type(order["id"]) is int and order["id"] > 0

    @allure.title("Поиск без трек-номера возвращает ошибку")
    def test_track_order_without_number(self, api):
        assert_error(api.track_order(), 400, ORDER_SEARCH_MISSING_DATA)

    @allure.title("Поиск по несуществующему трек-номеру возвращает ошибку")
    def test_track_order_with_nonexistent_number(self, api):
        assert_error(api.track_order(NONEXISTENT_ID), 404, ORDER_TRACK_NOT_FOUND)
