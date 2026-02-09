import requests
import json
from urls import BASE_URL, ORDERS_URL, ORDER_TRACK, ORDER_ACCEPT, ORDER_FINISH, ORDER_CANCEL
from data import HEADERS


class OrderMethods:
    
    def create_order(self, params):

        url = f'{BASE_URL}{ORDERS_URL}'
        response = requests.post(url, json=params, headers=HEADERS)
        
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code
    

    def get_order_by_track(self, track_number):

        url = f'{BASE_URL}{ORDER_TRACK}'
        params = {"t": track_number}
        response = requests.get(url, params=params, headers=HEADERS)
        
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code
    

    def get_orders_list(self, params=None):

        url = f'{BASE_URL}{ORDERS_URL}'
        response = requests.get(url, params=params, headers=HEADERS)
        
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code
    

    def accept_order(self, order_id, courier_id):

        url = f'{BASE_URL}{ORDER_ACCEPT}{order_id}'
        params = {"courierId": courier_id}
        response = requests.put(url, params=params, headers=HEADERS)
        
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code
    

    def finish_order(self, order_id):

        url = f'{BASE_URL}{ORDER_FINISH}{order_id}'
        response = requests.put(url, headers=HEADERS)
        
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code
    

    def cancel_order(self, track_number):

        url = f'{BASE_URL}{ORDER_CANCEL}'
        response = requests.put(url, json={"track": track_number}, headers=HEADERS)
        
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code
        

        