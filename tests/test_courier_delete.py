import allure

from scooter_api import (
    COURIER_DELETE_NOT_FOUND,
    NONEXISTENT_ID,
    ROUTE_NOT_FOUND,
    assert_error,
    assert_ok,
)


@allure.suite("Удаление курьера")
class TestCourierDelete:
    @allure.title("Удаление существующего курьера возвращает ok")
    def test_delete_existing_courier(self, api, courier_id):
        assert_ok(api.delete_courier(courier_id))

    @allure.title("Удаление без ID курьера возвращает ошибку")
    def test_delete_courier_without_id(self, api):
        assert_error(api.delete_courier(), 404, ROUTE_NOT_FOUND)

    @allure.title("Удаление несуществующего курьера возвращает ошибку")
    def test_delete_nonexistent_courier(self, api):
        assert_error(api.delete_courier(NONEXISTENT_ID), 404, COURIER_DELETE_NOT_FOUND)
