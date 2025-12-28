import requests

link = 'https://playground.learnqa.ru/api/long_redirect'


response = requests.get(link, allow_redirects=True)
print(f"Последний URL: {response.url}")

print(f"Всего редиректов: {len(response.history)}")

