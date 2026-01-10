from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserEdit(BaseCase):
    def setup_method(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        self.email = register_data['email']
        self.first_name = register_data['firstName']
        self.password = register_data['password']
        self.user_id = self.get_json_value(response1, 'id')

        # AUTHORIZATION
        login_data = {
            'email': self.email,
            'password': self.password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        self.auth_sid = self.get_cookie(response2, 'auth_sid')
        self.token = self.get_header(response2, 'x-csrf-token')

    def test_edit_just_created_user(self):
        # EDIT
        new_name = 'changedName'

        response = MyRequests.put(f'/user/{self.user_id}',
                                 cookies={'auth_sid': self.auth_sid},
                                 headers={'x-csrf-token': self.token},
                                 data={'firstName': new_name})
        Assertions.assert_status_code(response, 200)

        # GET
        response1 = MyRequests.get(f'/user/{self.user_id}',
                                 cookies={'auth_sid': self.auth_sid},
                                 headers={'x-csrf-token': self.token})
        Assertions.assert_json_value_by_name(response1,'firstName', new_name,"Values do not match")

    def test_edit_unauthorized_user(self):
        new_name = 'Even More Changed Name'

        response = MyRequests.put(f'/user/2',
                                   data={'firstName': new_name})
        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_value_by_name(response,'error', "Auth token not supplied","Response does not match")

    def test_edit_by_another_user(self):
        # EDIT
        new_name = 'Even More Changed Name2'

        response = MyRequests.put(f'/user/120065',
                                   cookies={'auth_sid': self.auth_sid},
                                   headers={'x-csrf-token': self.token},
                                   data={'firstName': new_name})

        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_value_by_name(response,'error', "This user can only edit their own data.","Response does not match")

    def test_edit_user_with_irregular_email(self):
        self.email = '12345example.com'

        response = MyRequests.put(f'/user/{self.user_id}',
                                   cookies={'auth_sid': self.auth_sid},
                                   headers={'x-csrf-token': self.token},
                                   data={'email': self.email})
        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_value_by_name(response, 'error', "Invalid email format",
                                             "Response does not match")

    def test_edit_user_with_short_firstname(self):
        # EDIT
        new_name = '1'

        response = MyRequests.put(f'/user/{self.user_id}',
                                   cookies={'auth_sid': self.auth_sid},
                                   headers={'x-csrf-token': self.token},
                                   data={'firstName': new_name})
        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_value_by_name(response, "error", "The value for field `firstName` is too short", "Response does not match")
