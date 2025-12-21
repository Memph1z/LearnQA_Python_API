import requests

payload = {"login": "secret_login", "password": "secret_pass"}
response = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)

cookie = response.cookies.get('auth_cookie')
cookies = {}
if cookie is not None:
    cookies.update({'auth_cookie': cookie})
response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

print(response2.text)
