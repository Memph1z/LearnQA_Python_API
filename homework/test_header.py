import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestCookie(BaseCase):

    def test_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        self.print_headers(response)
        Assertions.assert_header_value(response, "x-secret-homework-header", "Some secret value", "Header value doesn't match")