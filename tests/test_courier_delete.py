import allure

from data import COURIER_DELETE_NOT_FOUND, NONEXISTENT_ID, OK_RESPONSE, ROUTE_NOT_FOUND


@allure.suite("Удаление курьера")
class TestCourierDelete:
    @allure.title("Удаление существующего курьера возвращает ok")
    def test_delete_existing_courier(self, api, registered_courier):
        with allure.step("Удалить курьера по его ID"):
            response = api.delete_courier(registered_courier["id"])
        with allure.step("Проверить код 200 и тело ответа ok: true"):
            assert response.status_code == 200
            assert response.json() == OK_RESPONSE

    @allure.title("Удаление без ID курьера возвращает ошибку")
    def test_delete_courier_without_id(self, api):
        with allure.step("Отправить запрос на удаление без ID"):
            response = api.delete_courier()
        with allure.step("Проверить код 404 и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == ROUTE_NOT_FOUND

    @allure.title("Удаление несуществующего курьера возвращает ошибку")
    def test_delete_nonexistent_courier(self, api):
        with allure.step("Удалить курьера с несуществующим ID"):
            response = api.delete_courier(NONEXISTENT_ID)
        with allure.step("Проверить код 404 и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json()["message"] == COURIER_DELETE_NOT_FOUND
