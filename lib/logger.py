import datetime
import os

import allure
from requests import Response
import threading



class Logger:
    file_name = f"logs/log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"
    _lock = threading.Lock()

    @classmethod
    def _write_log_to_file(cls, data : str):
        with cls._lock:
            with open(cls.file_name, "a", encoding="utf-8") as logger_file:
                logger_file.write(data)

    @classmethod
    @allure.step("Сохраняем запрос в лог")
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        testname = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {testname}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Method: {method}\n"
        data_to_add += f"URL: {url}\n"
        data_to_add += f"Headers: {headers}\n"
        data_to_add += f"Cookies: {cookies}\n"
        data_to_add += f"Data: {data}\n"

        cls._write_log_to_file(data_to_add)

    @classmethod
    @allure.step("Делаем ответ запрос")
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += f"\n-----\n"

        cls._write_log_to_file(data_to_add)




