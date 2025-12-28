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