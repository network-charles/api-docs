import requests
import os

# Define the endpoint and headers
portfolio_id = "4567"  # The portfolio ID to be deleted
url = f"http://127.0.0.1:5000/financial-portfolio/{portfolio_id}"
DEFAULT_API_KEY = os.getenv('API_KEY')
headers = {
    "x-api-host": "finance-data.api.com",
    "x-api-key": DEFAULT_API_KEY
}

# Make the DELETE request
response = requests.delete(url, headers=headers)

# Print the status code and response data
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
