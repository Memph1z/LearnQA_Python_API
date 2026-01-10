import requests
from lib.logger import Logger
import allure
from environment import ENV_OBJECT

class MyRequests():
    @staticmethod
    @allure.step("Делаем GET запрос")
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"GET request with url: {url}"):
            return MyRequests._send(url, data, headers, cookies, 'GET')

    @staticmethod
    @allure.step("Делаем POST запрос")
    def post(url : str, data : dict = None, headers : dict = None, cookies : dict = None):
        with allure.step(f"POST request with url: {url}"):
            return MyRequests._send(url, data, headers, cookies, 'POST')

    @staticmethod
    @allure.step("Делаем DELETE запрос")
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"DELETE request with url: {url}"):
            return MyRequests._send(url, data, headers, cookies, 'DELETE')

    @staticmethod
    @allure.step("Делаем PUT запрос")
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"PUT request with url: {url}"):
            return MyRequests._send(url, data, headers, cookies, 'PUT')

    @staticmethod
    def _send(url : str, data : dict, headers : dict, cookies : dict, method : str):
        url = f"{ENV_OBJECT.get_base_url()}{url}"
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)

        if method == "GET":
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == "POST":
            response = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == "PUT":
            response = requests.put(url, data=data, headers=headers, cookies=cookies)
        elif method == "DELETE":
            response = requests.delete(url, data=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Method {method} not supported.")

        Logger.add_response(response)

        return response