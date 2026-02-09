import requests
import allure
import json
from urls import BASE_URL, COURIER_LOGIN
from data import HEADERS


class CourierLoginMethods:

    @allure.step('Авторизация курьера')
    def login_courier(self, params):

        url = f'{BASE_URL}{COURIER_LOGIN}'
        response = requests.post(url, json=params, headers=HEADERS)
        
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code