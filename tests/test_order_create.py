import allure
import pytest

from scooter_api import assert_json_response


@allure.suite("Создание заказа")
class TestOrderCreate:
    @allure.title("Создание заказа возвращает трек-номер ({param_id})")
    @pytest.mark.parametrize(
        "colors",
        [
            pytest.param(["BLACK"], id="BLACK"),
            pytest.param(["GREY"], id="GREY"),
            pytest.param(["BLACK", "GREY"], id="BLACK-and-GREY"),
            pytest.param(None, id="without-color"),
        ],
    )
    def test_create_order_returns_track(self, create_order, order_data, colors):
        if colors is not None:
            order_data["color"] = colors
        body = assert_json_response(create_order(order_data), 201)
        assert type(body["track"]) is int and body["track"] > 0
