import requests
import os

# Define the endpoint and headers
url = "http://127.0.0.1:5000/financial-portfolio"
DEFAULT_API_KEY = os.getenv('API_KEY')
headers = {
    "x-api-host": "finance-data.api.com",
    "x-api-key": DEFAULT_API_KEY,
    "Content-Type": "application/json"
}

# Define the JSON payload
data = {
    "portfolio_name": "Retirement Fund",
    "initial_balance": 50000
}

# Make the POST request
response = requests.post(url, headers=headers, json=data)

# Print the status code and response data
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
