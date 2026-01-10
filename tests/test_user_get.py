from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase

class TestUserGet(BaseCase):
    def test_get_user_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastname")

    def test_get_user_auth_as_same_user(self):
        data = {"email": "vinkotov@example.com",
                "password": "1234"
                }
        response1 = MyRequests.post("/user/login", data = data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_auth_as_another_user(self):
        data = {"email": "vinkotov@example.com",
                "password": "1234"
                }
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.get("/user/3",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        unexpected_fields = ["id", "email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_no_keys(response2, unexpected_fields)