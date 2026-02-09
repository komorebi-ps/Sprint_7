import pytest
import allure
from methods.order_methods import OrderMethods
from data import ORDER_DATA_1, ORDER_DATA_2, ORDER_DATA_3, ORDER_DATA_4

@allure.suite('Проверки создания заказа c черным цветом, серым цветом, обоими цветами и не выбрав цвет')
class TestOrderCreate:
    
    # Параметризация для заказа с двумя тестовыми наборами данных
    @pytest.mark.parametrize(
            "order_data", [ORDER_DATA_1, ORDER_DATA_2, ORDER_DATA_3, ORDER_DATA_4],
            ids = ['black', 'grey', 'both', 'none']
            )

    @allure.step('Проверка создания заказа с двумя наборами данных')
    def test_create_order_with_test_data(self, order_data):
        
        response_data, status_code = OrderMethods().create_order(order_data)
        
        assert status_code == 201, f"Expected 201, got {status_code}"
        assert 'track' in response_data, f"Response should contain 'track', got {response_data}"
        assert isinstance(response_data['track'], int), f"Track should be int, got {type(response_data['track'])}"



    @allure.step('Проверка получения списка заказов')
    def test_get_orders_list_basic(self):
        
        response_data, status_code = OrderMethods().get_orders_list()
        
        assert status_code == 200, f"Expected 200, got {status_code}"
        assert 'orders' in response_data, f"Should contain 'orders' field"
        assert isinstance(response_data['orders'], list), "'orders' should be a list"
        