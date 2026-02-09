import pytest
import allure
from methods.courier_create_methods import CourierCreateMethods
from methods.courier_login_methods import CourierLoginMethods
from data import COURIER_DATA_WITHOUT_LOGIN, COURIER_DATA_WITHOUT_PASSWORD, COURIER_DATA_WITHOUT_FIRSTNAME
from helpers import generate_random_string

@allure.suite('Проверки на создание курьеров')
class TestCourierCreate:
    

    @allure.title('Проверка возможности создания курьера и получения ответа {"ok":true}')
    def test_courier_can_be_created(self):
        
        # Создаем курьера
        courier_data, response_data, status_code = CourierCreateMethods().register_new_courier_and_return_login_password()
        
        assert len(courier_data) == 3, f"Expected list of 3 items, got {len(courier_data)}"
        assert status_code == 201, f"Expected 201 for создания курьера без firstName, got {status_code}"
        assert response_data == {"ok": True}, f"Expected {{'ok': True}}, got {response_data}"

        # Логинимся, чтобы получить ID
        login_response, login_status = CourierLoginMethods().login_courier({
            "login": courier_data[0],
            "password": courier_data[1]
        })
        
        # Удаляем курьера
        if login_status == 200 and 'id' in login_response:
            CourierCreateMethods().delete_courier(login_response['id'])
    


    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_cant_create_two_identical_couriers(self):
        
        # Создаем первого курьера 
        login = "test_duplicate_login"
        password = "test_password"
        first_name = "Courier"
        
        courier_data = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        first_response, first_status = CourierCreateMethods().create_courier(courier_data)
        
        # Пытаемся создать второго курьера с такими же данными
        second_response, second_status = CourierCreateMethods().create_courier(courier_data)

        assert second_status == 409, f"Expected 409 for duplicate, got {second_status}"
        assert isinstance(second_response, dict), f"Response should be dict, got {type(second_response)}"
        expected_message = "Этот логин уже используется. Попробуйте другой."
        actual_message = second_response.get("message")
        assert actual_message == expected_message, f"Expected message: '{expected_message}', got: '{actual_message}'"
        
        # Очистка: удаляем созданного курьера
        login_response, login_status = CourierLoginMethods().login_courier({
            "login": login,
            "password": password
        })
        
        if login_status == 200 and 'id' in login_response:
            CourierCreateMethods().delete_courier(login_response['id'])
    


    @allure.title('Проверка создания курьера со всеми обязательными полями но без необязательного')
    def test_create_courier_with_required_fields_only(self):

        response_data, status_code = CourierCreateMethods().create_courier(COURIER_DATA_WITHOUT_FIRSTNAME)

        assert status_code == 201, f"Expected 201 for создания курьера без firstName, got {status_code}"
        assert "ok" in response_data, f"Successful response should contain 'ok', got {response_data}"

        login_response, login_status = CourierLoginMethods().login_courier({
        "login": COURIER_DATA_WITHOUT_FIRSTNAME["login"],
        "password": COURIER_DATA_WITHOUT_FIRSTNAME["password"]
        })

        if login_status == 200 and 'id' in login_response:
            CourierCreateMethods().delete_courier(login_response['id'])[1]


    # Параметризация для проверки создания курьера без одного из полей
    @pytest.mark.parametrize(
        'test_data, description', 
        [
            (COURIER_DATA_WITHOUT_LOGIN, 'без логина'),
            (COURIER_DATA_WITHOUT_PASSWORD, 'без пароля'),
        ],
        ids = ['missing_login', 'missing_password'] 
    )

    @allure.title('Проверка получения ошибки при попытке создания курьера без обязательного поля')
    @allure.description('Поочередно проверяем получение ошибки при создании курьера сначала без логина, потом без пароля')
    def test_create_courier_without_required_field_fails(self, test_data, description):
        
        response_data, status_code = CourierCreateMethods().create_courier(test_data)
        
        assert status_code == 400, f"Expected 400 for {description}, got {status_code}"
        assert isinstance(response_data, dict), f"Response should be dict, got {type(response_data)}"
        expected_message = "Недостаточно данных для создания учетной записи"
        actual_message = response_data.get("message")
        assert actual_message == expected_message, f"Expected message: '{expected_message}', got: '{actual_message}'"

    
    @allure.title('Проверка получения ошибки при попытке создать курьера с уже существующим логином')
    def test_existing_login_returns_error(self):
        
        # Создаем первого курьера
        login = "test_existing_login"
        password = "test_password"
        first_name = "Test User"
        
        first_courier_data = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        first_response, first_status = CourierCreateMethods().create_courier(first_courier_data)
        
        # Создаем второго курьера с таким же логином, но другими данными
        second_courier_data = {
            "login": login,
            "password": "different_password",
            "firstName": "Different Name"
        }
        
        second_response, second_status = CourierCreateMethods().create_courier(second_courier_data)
        assert second_status == 409, f"Expected 409 for existing login, got {second_status}"
        assert isinstance(second_response, dict), f"Response should be dict, got {type(second_response)}"
        expected_message = "Этот логин уже используется. Попробуйте другой."
        actual_message = second_response.get("message")
        assert actual_message == expected_message, f"Expected message: '{expected_message}', got: '{actual_message}'"
        
        # Очистка
        login_response, login_status = CourierLoginMethods().login_courier({
            "login": login,
            "password": password
        })
        
        if login_status == 200 and 'id' in login_response:
            CourierCreateMethods().delete_courier(login_response['id'])