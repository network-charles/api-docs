import requests
import os

# Define the endpoint and headers
url = "http://127.0.0.1:5000/currency-exchange-rate"
DEFAULT_API_KEY = os.getenv('API_KEY')
headers = {
    "x-rapidapi-host": "finance-data.api.com",
    "x-rapidapi-key": DEFAULT_API_KEY
}
params = {
    "from_symbol": "USD",
    "to_symbol": "NGN"
}

# Make the GET request
response = requests.get(url, headers=headers, params=params)

# Print the status code and response data
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
