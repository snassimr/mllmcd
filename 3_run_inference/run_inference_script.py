import requests
import json

def send_post_request(url, data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)

        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None

if __name__ == "__main__":
    url = 'http://localhost:8080/generate'  # Replace with your URL
    payload = {'key': 'value'}

    response = send_post_request(url, payload)

    if response:
        print(f'Success: {response}')
    else:
        print('Failed to get a valid response.')
