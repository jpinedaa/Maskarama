import requests

# URL of the endpoint
url = 'http://localhost:5500/api/user_input'  # Replace with the correct URL if different

# JSON payload to send in the request
payload = {
    "input": "make hermes slip and fall"  # Replace with the actual input you want to test
}

# Send the POST request
response = requests.post(url, json=payload)

# Print the response
print(f'Status Code: {response.status_code}')
print(f'Response JSON: {response.json()}')
