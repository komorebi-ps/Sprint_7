import pytest
import allure
from methods.courier_create_methods import CourierCreateMethods
from methods.courier_login_methods import CourierLoginMethods
from data import LOGIN_DATA_WITHOUT_LOGIN, LOGIN_DATA_WITHOUT_PASSWORD

@allure.suite('Проверки на авторизацию курьеров')
class TestCourierLogin:
    
    @allure.title('Проверка авторизации и получения id в теле ответа')
    def test_courier_can_login(self):
        
        # Создаем курьера
        courier_data, response_data, status_code = CourierCreateMethods().register_new_courier_and_return_login_password()
        
        # Логинимся
        login_response, login_status = CourierLoginMethods().login_courier({
        "login": courier_data[0],
        "password": courier_data[1]
    })
        
        # Проверяем успешную авторизацию
        assert login_status == 200, f"Expected 200, got {login_status}"
        assert 'id' in login_response, f"Response should contain 'id', got {login_response}"
        
        # Удаляем курьера
        CourierCreateMethods().delete_courier(login_response['id'])
    


    # Параметризация для проверки логина без одного из полей
    @pytest.mark.parametrize(
        'test_data, description', 
        [
            (LOGIN_DATA_WITHOUT_LOGIN, 'без логина'),
            (LOGIN_DATA_WITHOUT_PASSWORD, 'без пароля'),
        ],
        ids=['missing_login', 'missing_password'] 
    )

    @allure.title('Проверка получения ошибки при попытке авторизации без одного из обязательных полей')
    def test_login_requires_all_fields(self, test_data, description):

        response_data, status_code = CourierLoginMethods().login_courier(test_data)       

        assert status_code == 400, f"Expected 400 for {description}, got {status_code}"
        expected_message = "Недостаточно данных для входа"
        actual_message = response_data.get("message")
        assert actual_message == expected_message, f"Expected message: '{expected_message}', got: '{actual_message}' for {description}"
    

    @allure.title('Проверка получения ошибки при указании неверного логина или пароля')
    def test_wrong_login_or_password_returns_error(self):
        
        # Создаем курьера
        courier_data = CourierCreateMethods().register_new_courier_and_return_login_password()
        
        if not courier_data or len(courier_data) < 3:
            pytest.fail("Не удалось создать курьера для теста")
        
        # Пытаемся залогиниться с неправильным паролем
        wrong_login_data = {
            "login": courier_data[0],
            "password": "wrong_password"
        }
        
        response_data, status_code = CourierLoginMethods().login_courier(wrong_login_data)
        
        assert status_code == 404, f"Expected 404 for wrong credentials, got {status_code}"
        expected_message = "Учетная запись не найдена"
        actual_message = response_data.get("message")
        assert actual_message == expected_message, f"Expected message: '{expected_message}', got: '{actual_message}'"
        
        # Очистка: логинимся с правильными данными и удаляем курьера
        correct_login_data = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        
        login_response, login_status = CourierLoginMethods().login_courier(correct_login_data)
        if login_status == 200 and 'id' in login_response:
            CourierCreateMethods().delete_courier(login_response['id'])


    @allure.title('Проверка получения ошибки при попытке авторизации под не существующим пользователем')
    def test_nonexistent_user_returns_error(self):

        nonexistent_user = {
            "login": "nonexistent_user_1234567890",
            "password": "password123"
        }
        
        response_data, status_code = CourierLoginMethods().login_courier(nonexistent_user)
        
        assert status_code == 404, f"Expected 404 for wrong credentials, got {status_code}"
        expected_message = "Учетная запись не найдена"
        actual_message = response_data.get("message")
        assert actual_message == expected_message, f"Expected message: '{expected_message}', got: '{actual_message}'"
    
