HEADERS = {
    'Content-Type': 'application/json'
}

# Наборы данных для заказов (для параметризации)
ORDER_DATA_1 = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha",
    "color": ["BLACK"]
}

ORDER_DATA_2 = {
    "firstName": "Sasuke",
    "lastName": "Uchiha",
    "address": "Orochimaru's hideout, 1 apt.",
    "metroStation": 2,
    "phone": "+7 900 123 45 67",
    "rentTime": 3,
    "deliveryDate": "2024-12-31",
    "comment": "I need power",
    "color": ["GREY"]
}

ORDER_DATA_3 = {
    "firstName": "Paul",
    "lastName": "Newman",
    "address": "Mndjrjgge, 234 apt.",
    "metroStation": 1,
    "phone": "+7 234 654 65 45",
    "rentTime": 10,
    "deliveryDate": "2025-12-05",
    "comment": "Comment123324",
    "color": ["GREY", "BLACK"]
}

ORDER_DATA_4 = {
        "firstName": "Paul",
    "lastName": "Newman",
    "address": "Mndjrjgge, 234 apt.",
    "metroStation": 1,
    "phone": "+7 234 654 65 45",
    "rentTime": 10,
    "deliveryDate": "2025-12-05",
    "comment": "Comment123324",
    "color": []
}

# Данные для неполных запросов курьера
COURIER_DATA_WITHOUT_LOGIN = {
    "password": "1234",
    "firstName": "saske_test"
}

COURIER_DATA_WITHOUT_PASSWORD = {
    "login": "kjfhrtiunbruib",
    "firstName": "Kjrevkbf"
}

COURIER_DATA_WITHOUT_FIRSTNAME = {
    "login": "uyhnrgituge",
    "password": "45876948"
}

# Данные для неполных запросов логина
LOGIN_DATA_WITHOUT_LOGIN = {
    "password": "1234"
}

LOGIN_DATA_WITHOUT_PASSWORD = {
    "login": "gtjrkjtgn"
}