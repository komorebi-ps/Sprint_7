import requests
import json
import random
import string
from urls import BASE_URL, COURIER_URL
from data import HEADERS
from helpers import generate_random_string
import allure


class CourierCreateMethods:
    
    @allure.step('Создаем нового курьера c рандомными данными и возвращаем логин+пароль')
    def register_new_courier_and_return_login_password(self):

        # создаём список, чтобы метод мог его вернуть
        login_pass = []

        # генерируем логин, пароль и имя курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # отправляем запрос на регистрацию курьера
        response = requests.post(f'{BASE_URL}{COURIER_URL}', json=payload, headers=HEADERS)

        # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)

        # возвращаем список
        return login_pass, response.json(), response.status_code
    

    @allure.step('Создаем курьера')
    def create_courier(self, params=None):

        if params is None:
            # Генерируем случайные данные
            login = self.generate_random_string(10)
            password = self.generate_random_string(10)
            first_name = self.generate_random_string(10)
            
            params = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            
        url = f'{BASE_URL}{COURIER_URL}'
        response = requests.post(url, json=params, headers=HEADERS)
        
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code
    
    @allure.step('Удаляем курьера')
    def delete_courier(self, courier_id):

        url = f'{BASE_URL}{COURIER_URL}{courier_id}'
        response = requests.delete(url, headers=HEADERS)
        
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code
    

    @allure.step('Получаем количество заказов курьера')
    def get_courier_orders_count(self, courier_id):

        url = f'{BASE_URL}{COURIER_URL}{courier_id}/ordersCount'
        response = requests.get(url, headers=HEADERS)
        
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code