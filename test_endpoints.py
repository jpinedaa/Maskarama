import requests

# URL of the endpoint
#addr = 'http://54.221.38.133:5500/'
addr = 'http://localhost:5500/'
# endpoint = 'api/user_input'  # Replace with the correct URL if different
#
# # JSON payload to send in the request
# payload = {
#     "input": "make hermes slip and fall"  # Replace with the actual input you want to test
# }

endpoint = 'api/api_key'

payload = {
    "key": "testing"
}


# Send the POST request
response = requests.post(addr + endpoint, json=payload)

# Print the response
print(f'Status Code: {response.status_code}')
print(f'Response JSON: {response.json()}')

