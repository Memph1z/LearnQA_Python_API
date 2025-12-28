import requests
import time

link = "https://playground.learnqa.ru/ajax/api/longtime_job"

response = requests.get(link)
print(response.text)

token = response.json()["token"]
seconds = response.json()["seconds"]

wrong_time_request = requests.get(link, params={"token": f"{token}"})
print(wrong_time_request.text)

time.sleep(seconds)

right_time_request = requests.get(link, params={"token": f"{token}"})

data = right_time_request.json()
if 'result' not in data and data.get('status') != "Job is ready" :
    print("Джоба не успела отработать или произошла другая ошибка")
else:
    print(right_time_request.text)
    print("Джоба отработала успешно!")

