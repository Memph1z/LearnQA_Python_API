import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestCookie(BaseCase):

    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        self.print_cookies(response)
        Assertions.assert_cookie_value(response, "HomeWork", "hw_value", "Cookie value doesn't match")