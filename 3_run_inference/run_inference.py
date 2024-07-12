import requests
import json

url = 'http://localhost:8080/generate'  # Replace with your URL

payload = {
    'key': 'value'
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print(f'Status Code: {response.status_code}')
print(f'Response: {response.json()}')
