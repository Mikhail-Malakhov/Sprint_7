DEFAULT_API_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

COURIER_PATH = "/courier"
COURIER_LOGIN_PATH = "/courier/login"
ORDERS_PATH = "/orders"
ORDER_TRACK_PATH = "/orders/track"
ORDER_ACCEPT_PATH = "/orders/accept"
ORDER_CANCEL_PATH = "/orders/cancel"
ORDER_FINISH_PATH = "/orders/finish"

REQUEST_TIMEOUT = 25
LONG_REQUEST_TIMEOUT = 75
CONNECT_TIMEOUT = 5
GATEWAY_ERROR_CODES = (502, 503, 504)

NONEXISTENT_ID = 2_147_483_647

COURIER_LOGIN_PREFIX = "sprint7_"
COURIER_FIRST_NAME = "Тестовый курьер"
ANOTHER_COURIER_FIRST_NAME = "Другой курьер"
INVALID_VALUE_PREFIX = "invalid_"

ORDER_DATA = {
    "firstName": "Тестовый",
    "lastName": "Заказ",
    "address": "Тестовая улица, 1",
    "metroStation": "4",
    "phone": "+70000000000",
    "rentTime": 1,
}
ORDER_DELIVERY_DAYS = 2
ORDER_COMMENT_PREFIX = "Sprint 7: "
ORDER_COLORS = {
    "BLACK": ["BLACK"],
    "GREY": ["GREY"],
    "BLACK-and-GREY": ["BLACK", "GREY"],
}

OK_RESPONSE = {"ok": True}

COURIER_CREATE_MISSING_DATA = "Недостаточно данных для создания учетной записи"
COURIER_LOGIN_ALREADY_USED = "Этот логин уже используется. Попробуйте другой."
COURIER_LOGIN_MISSING_DATA = "Недостаточно данных для входа"
COURIER_ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
COURIER_DELETE_NOT_FOUND = "Курьера с таким id нет."
ROUTE_NOT_FOUND = "Not Found."
ORDER_SEARCH_MISSING_DATA = "Недостаточно данных для поиска"
ORDER_TRACK_NOT_FOUND = "Заказ не найден"
ORDER_ID_NOT_FOUND = "Заказа с таким id не существует"
ORDER_COURIER_NOT_FOUND = "Курьера с таким id не существует"
