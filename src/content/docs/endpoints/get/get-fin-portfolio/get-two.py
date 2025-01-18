import requests
import os

# Input the portfolio ID
portfolio_id = "YOUR_PORTFOLIO_ID"
# Define the endpoint and URL
url = f"http://127.0.0.1:5000/financial-portfolio/{portfolio_id}"
DEFAULT_API_KEY = os.getenv('API_KEY')
headers = {
    "x-api-host": "finance-data.api.com",
    "x-api-key": DEFAULT_API_KEY
}

# Make the GET request
response = requests.get(url, headers=headers)

# Print the status code and response data
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
