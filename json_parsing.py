import requests
from json.decoder import JSONDecodeError

response = requests.get("https://playground.learnqa.ru/api/get_text")
try:
    parsed_response = response.json()
    print(parsed_response)
except JSONDecodeError:
    print("Response in not a JSON format")
