from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import  Assertions
import pytest

class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data = data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data = data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content '{response.content}'"

    def test_user_incorrect_email(self):
        email = 'wtfisthis.example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data = data)
        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Unexpected response content '{response.content}'"

    def test_user_short_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = '1'

        response = MyRequests.post("/user", data = data)
        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'firstName' field is too short", f"Unexpected response content '{response.content}'"

    def test_user_long_name(self):
        data = self.prepare_registration_data()
        data['lastName'] = 'fihitjbxeegigugymfnjzfxcjeynrzerhaeictzarnkkenuvmfraeudjtmankcxguadzuuyueiwxrmaiiwvyeztwpecwmzkwimceimpaubxjpxfjzhvqmzdvjihetjaubzavmpqeykvzxicqzuifvzxtxfhnmixmrewcwupwtewvqmptgueaqmcbvfkgrrmrqcqivnubccdrnfmugaajcaavwcvnnivkwrgiaznhrhbjkbxnhkactfizxdj'

        response = MyRequests.post("/user", data = data)
        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'lastName' field is too long", f"Unexpected response content '{response.content}'"

    @pytest.mark.parametrize("condition", ["password", "username", "firstName", "lastName", "email"])
    def test_missing_data_fields(self, condition):
        data = self.prepare_registration_data()
        data.pop(condition)

        response = MyRequests.post("/user", data=data)
        Assertions.assert_status_code(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {condition}", f"Unexpected response content '{response.content}'"