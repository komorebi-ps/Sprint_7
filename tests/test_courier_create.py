import pytest
import allure
from methods.courier_create_methods import CourierCreateMethods
from methods.courier_login_methods import CourierLoginMethods
from data import COURIER_DATA_WITHOUT_LOGIN, COURIER_DATA_WITHOUT_PASSWORD, COURIER_DATA_WITHOUT_FIRSTNAME

@allure.suite('Проверки на создание курьеров')
class TestCourierCreate:
    

    @allure.step('Проверка возможности создания курьера')
    def test_courier_can_be_created(self):
        
        # Используем метод с генерацией данных
        courier_data = CourierCreateMethods().register_new_courier_and_return_login_password()
        
        # Проверяем, что курьер создан 
        assert len(courier_data) == 3, f"Expected list of 3 items, got {len(courier_data)}"
        assert courier_data[0]  # login
        assert courier_data[1]  # password
        assert courier_data[2]  # first_name
        
        # Логинимся, чтобы получить ID
        login_response, login_status = CourierLoginMethods().login_courier({
            "login": courier_data[0],
            "password": courier_data[1]
        })
        
        assert login_status == 200, f"Login should return 200, got {login_status}"
        assert 'id' in login_response, f"Response should contain 'id', got {login_response}"
        
        # Удаляем курьера
        delete_response, delete_status = CourierCreateMethods().delete_courier(login_response['id'])
        assert delete_status == 200, f"Delete should return 200, got {delete_status}"
    


    @allure.step('Проверка невозможности создания двух одинаковых курьеров')
    def test_cant_create_two_identical_couriers(self):
        
        # Создаем первого курьера с конкретными данными
        login = "test_duplicate_login"
        password = "test_password"
        first_name = "Courier"
        
        courier_data = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        # Создаем первого курьера
        first_response, first_status = CourierCreateMethods().create_courier(courier_data)
        assert first_status == 201, f"First creation should be 201, got {first_status}"
        
        # Пытаемся создать второго курьера с такими же данными
        second_response, second_status = CourierCreateMethods().create_courier(courier_data)
        assert second_status == 409, f"Expected 409 for duplicate, got {second_status}"
        assert "message" in second_response, f"Response should contain message, got {second_response}"
        
        # Очистка: удаляем созданного курьера
        login_response, login_status = CourierLoginMethods().login_courier({
            "login": login,
            "password": password
        })
        
        if login_status == 200 and 'id' in login_response:
            CourierCreateMethods().delete_courier(login_response['id'])
    


    @allure.step('Проверка создания курьера со всеми обязательными полями')
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

    @allure.step('Проверка получения ошибки при попытке создания курьера без обязательного поля')
    def test_create_courier_without_required_field_fails(self, test_data, description):
        
        response_data, status_code = CourierCreateMethods().create_courier(test_data)
        
        assert status_code == 400, f"Expected 400 for {description}, got {status_code}"
        if isinstance(response_data, dict):
            assert "message" in response_data, f"Response should contain 'message' for {description}, got {response_data}"
    

    @allure.step('Проверка того, что запрос возвращает корректный статус ответа')
    def test_request_returns_correct_status_code(self):
        
        # Создаем курьера
        response_data, status_code = CourierCreateMethods().create_courier()
        
        # Проверяем успешный код ответа
        assert status_code == 201, f"Expected 201, got {status_code}"
        
        # Получаем данные созданного курьера для удаления
        # Для этого нужно залогиниться, но у нас нет данных
        # Вместо этого используем метод register_new_courier_and_return_login_password
        courier_data = CourierCreateMethods().register_new_courier_and_return_login_password()
        if len(courier_data) == 3:
            login_response, login_status = CourierLoginMethods().login_courier({
                "login": courier_data[0],
                "password": courier_data[1]
            })
            
            if login_status == 200 and 'id' in login_response:
                CourierCreateMethods().delete_courier(login_response['id'])
    

    @allure.step('Проверка успешного ответа при создании курьера')
    def test_successful_request_returns_ok_true(self):

        login = CourierCreateMethods().generate_random_string(10)
        password = CourierCreateMethods().generate_random_string(10)
        first_name = CourierCreateMethods().generate_random_string(10)
    
        test_courier_data = {
        "login": login,
        "password": password,
        "firstName": first_name
        }
        response_data, status_code = CourierCreateMethods().create_courier(test_courier_data)

        assert status_code == 201, f"Expected 201, got {status_code}"
        assert response_data == {"ok": True}, f"Expected {{'ok': True}}, got {response_data}"

        # Очистка
        login_response, login_status = CourierLoginMethods().login_courier({
        "login": login,
        "password": password
        })
        if login_status == 200 and 'id' in login_response:
            CourierCreateMethods().delete_courier(login_response['id'])
    
    @allure.step('Проверка получения ошибки при попытке создать курьера с уже существующим логином')
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
        assert first_status == 201, f"First creation should be 201, got {first_status}"
        
        # Создаем второго курьера с таким же логином, но другими данными
        second_courier_data = {
            "login": login,
            "password": "different_password",
            "firstName": "Different Name"
        }
        
        second_response, second_status = CourierCreateMethods().create_courier(second_courier_data)
        assert second_status == 409, f"Expected 409 for existing login, got {second_status}"
        assert "message" in second_response, f"Response should contain message, got {second_response}"
        
        # Очистка
        login_response, login_status = CourierLoginMethods().login_courier({
            "login": login,
            "password": password
        })
        
        if login_status == 200 and 'id' in login_response:
            CourierCreateMethods().delete_courier(login_response['id'])