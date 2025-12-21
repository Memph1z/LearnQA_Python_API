import requests

response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
response1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
print(response1.text)
response2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "HEAD"})
print(response2.text)

http_methods = ["GET", "POST", "PUT", "DELETE"]

for req_method in http_methods:
    print(f"Проверяем тип запроса {req_method}")
    for method in http_methods:
        if req_method == "GET":
            response = requests.request(req_method,"https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": method})
        else:
            response = requests.request(req_method,"https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": method})

        print(f"{req_method} + {method} = {response.text}")
