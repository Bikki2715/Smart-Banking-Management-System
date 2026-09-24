'''
import requests

url = "http://127.0.0.1:50001/api/admin/change-account-status"

data = {
    "account_no": 100001,
    "new_status": "Active"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())

'''


import requests

url = "http://127.0.0.1:50001/api/admin/login"

data = {
    "username": "admin",
    "password": "admin123"
}

response = requests.post(
    url,
    json=data
)

print(response.status_code)
print(response.json())