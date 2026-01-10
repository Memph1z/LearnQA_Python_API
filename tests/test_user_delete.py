import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserDelete(BaseCase):
    def test_delete_undeletable_user(self):
        data = {"email": "vinkotov@example.com",
                "password": "1234"
                }

        response = MyRequests.post("/user/login", data = data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        response1 = MyRequests.delete("/user/2",
                                      cookies={'auth_sid': auth_sid},
                                      headers={'x-csrf-token': token})
        Assertions.assert_status_code(response1, 400)
        Assertions.assert_json_value_by_name(response1,'error', "Please, do not delete test users with ID 1, 2, 3, 4 or 5.","Response does not match")

    def test_delete_just_created_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # AUTHORIZATION
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      cookies={'auth_sid': auth_sid},
                                      headers={'x-csrf-token': token})
        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequests.get(f'/user/{user_id}',
                                   cookies={'auth_sid': auth_sid},
                                   headers={'x-csrf-token': token})
        Assertions.assert_status_code(response4, 404)

    def test_delete_other_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']

        # AUTHORIZATION
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # DELETE
        response3 = MyRequests.delete(f"/user/11",
                                      cookies={'auth_sid': auth_sid},
                                      headers={'x-csrf-token': token})
        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_value_by_name(response3,'error', "This user can only delete their own account.","Response does not match")
