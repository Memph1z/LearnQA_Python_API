from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response : Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response is '{response.text}'"

        assert name in response_as_dict, f"Response does not contain '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response : Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response is '{response.text}'"

        assert name in response_as_dict, f"Response does not contain '{name}'"

    @staticmethod
    def assert_json_has_keys(response : Response, names : list):
        for name in names:
            Assertions.assert_json_has_key(response, name)

    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response is '{response.text}'"

        assert name not in response_as_dict, f"Response does contain '{name}', when it shouldn't"

    @staticmethod
    def assert_status_code(response : Response, status_code):
        assert response.status_code == status_code, f"Response status code does not match '{status_code}'"

    @staticmethod
    def assert_phrase_is_less_than_15_symbols(phrase, error_message):
        assert len(phrase) < 15, error_message

    @staticmethod
    def assert_cookie_value(response : Response, cookie_name, cookie_value, error_message):
        assert cookie_name in response.cookies, f"{cookie_name} not found in cookies"
        assert response.cookies[cookie_name] == cookie_value, error_message

    @staticmethod
    def assert_header_value(response: Response, header_name, header_value, error_message):
        assert header_name in response.headers, f"{header_name} not found in response"
        assert response.headers[header_name] == header_value, error_message