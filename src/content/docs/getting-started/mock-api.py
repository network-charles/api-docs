import os
from flask import Flask, jsonify, request
import time
import datetime
from collections import defaultdict
import random

app = Flask(__name__)

DEFAULT_API_KEY = os.getenv('API_KEY')

# Rate-limiting data structure
request_log = defaultdict(list)
RATE_LIMIT = 5  # Max requests per time window
TIME_WINDOW = 60  # Time window in seconds (e.g., 60 seconds = 1 minute)

# For HTTP 409 Error
def check_rate_limit():
    # Rate limiting: Check if the request exceeds the rate limit
    client_ip = request.remote_addr
    current_time = time.time()
    
    # Remove timestamps older than the time window (rate-limiting)
    request_log[client_ip] = [timestamp for timestamp in request_log[client_ip] if current_time - timestamp < TIME_WINDOW]

    # Check if the number of requests exceeds the rate limit
    if len(request_log[client_ip]) >= RATE_LIMIT:
        return jsonify({"error": "Too many requests"}), 429  # Too Many Requests

    # Log the current request timestamp
    request_log[client_ip].append(current_time)
    
# For HTTP 5xx Errors
def simulate_server_errors(param1, param2):
    """
    Simulate different server errors based on the values of two parameters.
    Args:
        param1: The first parameter to check (e.g., 'from_symbol').
        param2: The second parameter to check (e.g., 'to_symbol').
    Returns:
        A tuple (response, status_code) if an error is simulated, or None if no error occurs.
    """
    if param1 == "500" or param2 == "500":
        return jsonify({"error": "Internal server error"}), 500  # 500 Internal Server Error

    if param1 == "502" or param2 == "502":
        return jsonify({"error": "Bad Gateway"}), 502  # 502 Bad Gateway

    if param1 == "503" or param2 == "503":
        return jsonify({"error": "Service Unavailable"}), 503  # 503 Service Unavailable

    if param1 == "504" or param2 == "504":
        return jsonify({"error": "Gateway Timeout"}), 504  # 504 Gateway Timeout

    return None

@app.route('/currency-exchange-rate', methods=['GET'])
def mock_currency_exchange_rate():
    # Get query parameters and headers
    from_symbol = request.args.get('from_symbol')
    to_symbol = request.args.get('to_symbol')
    api_host = request.headers.get('x-api-host')
    api_key = request.headers.get('x-api-key')

    # Check for missing or invalid headers
    if not api_host or not api_key:
        return jsonify({"error": "Missing required headers"}), 401  # Unauthorized

    if api_host != "finance-data.api.com":
        return jsonify({"error": "Invalid x-api-host"}), 403  # Forbidden

    if api_key != "1234567890":
        return jsonify({"error": "Invalid API key"}), 403  # Forbidden

    # Check rate limit
    rate_limit_response = check_rate_limit()
    if rate_limit_response:
        return rate_limit_response

    # Check for missing query parameters
    if not from_symbol or not to_symbol:
        return jsonify({"error": "Missing required query parameters 'from_symbol' or 'to_symbol'"}), 400  # Bad Request

    # Simulate external service failure (e.g., unavailable exchange rate service)
    if from_symbol == "SERVICE_UNAVAILABLE" or to_symbol == "SERVICE_UNAVAILABLE":
        return jsonify({"error": "The external service is unavailable. Please try again later."}), 402  # Request Failed

    # Simulate 404 Not Found based on specific conditions
    if from_symbol == "NOT_FOUND" or to_symbol == "NOT_FOUND":
        return jsonify({"error": "Resource not found"}), 404  # Not Found

    # Check for conflict: from_symbol is the same as to_symbol
    if from_symbol == to_symbol:
        return jsonify({"error": "Conflict: Cannot exchange the same currency"}), 409  # Conflict

    # Check for server errors
    error_response = simulate_server_errors(from_symbol, to_symbol)
    if error_response:
        return error_response

    # Get current UTC time
    current_utc_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Generate random exchange rate and previous close within a range
    exchange_rate = round(random.uniform(1550.00, 1600.00), 4)  # Random value between 1550 and 1600
    previous_close = round(random.uniform(1500.00, 1550.00), 2)  # Random value between 1500 and 1550

    # Default success response
    return jsonify({
        "status": "OK",
        "request_id": "59f8125c-90a1-4d33-a139-67b83b09017e",
        "data": {
            "from_symbol": from_symbol,
            "to_symbol": to_symbol,
            "type": "currency",
            "exchange_rate": exchange_rate,
            "previous_close": previous_close,
            "last_update_utc": current_utc_time
        }
    }), 200

# Portfolio data structure
portfolios = {}

# New POST endpoint: Create a new financial portfolio
@app.route('/financial-portfolio', methods=['POST'])
def create_portfolio():

    # Validate headers directly
    api_host = request.headers.get('x-api-host')
    api_key = request.headers.get('x-api-key')

    if not api_host or not api_key:
        return jsonify({"error": "Missing required headers"}), 401  # Unauthorized

    if api_host != "finance-data.api.com":
        return jsonify({"error": "Invalid x-api-host"}), 403  # Forbidden

    if api_key != DEFAULT_API_KEY:
        return jsonify({"error": "Invalid API key"}), 403  # Forbidden

    # Check rate limit
    rate_limit_response = check_rate_limit()
    if rate_limit_response:
        return rate_limit_response
    
    data = request.get_json()
    
    portfolio_name = data['portfolio_name']
    initial_balance = data['initial_balance']

    # Check for missing query parameters
    if not portfolio_name or not initial_balance:
        return jsonify({"error": "Missing required query parameters 'portfolio_name' or 'initial_balance'"}), 400  # Bad Request

    # Check for server errors
    error_response = simulate_server_errors(portfolio_name, None)
    if error_response:
        return error_response

    # Simulate creating a portfolio with an ID and an initial balance
    portfolio_id = str(random.randint(1000, 9999))
    creation_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Store the portfolio in the portfolios dictionary
    portfolios[portfolio_id] = {
        "portfolio_id": portfolio_id,
        "portfolio_name": portfolio_name,
        "initial_balance": initial_balance,
        "creation_time": creation_time
    }

    # Simulate external service failure
    if portfolio_name == "SERVICE_UNAVAILABLE":
        return jsonify({"error": "The external service is unavailable. Please try again later."}), 402  # Request Failed
    
    return jsonify({
        "status": "OK",
        "message": "Portfolio created successfully",
        "portfolio": portfolios[portfolio_id]
    }), 201  # Created

# New GET endpoint: Retrieve a portfolio by ID
@app.route('/financial-portfolio/<portfolio_id>', methods=['GET'])
def get_portfolio(portfolio_id):

    # Validate headers directly
    api_host = request.headers.get('x-api-host')
    api_key = request.headers.get('x-api-key')

    if not api_host or not api_key:
        return jsonify({"error": "Missing required headers 'api_host' or 'api_key'"}), 401  # Unauthorized

    if api_host != "finance-data.api.com":
        return jsonify({"error": "Invalid x-api-host"}), 403  # Forbidden

    if api_key != DEFAULT_API_KEY:
        return jsonify({"error": "Invalid API key"}), 403  # Forbidden

    # Check rate limit
    rate_limit_response = check_rate_limit()
    if rate_limit_response:
        return rate_limit_response

    # Retrieve the portfolio from the portfolios dictionary
    portfolio = portfolios.get(portfolio_id)

    # Check for missing query parameters
    if not portfolio:
        return jsonify({"error": "Missing required query parameters 'portfolio_id'"}), 400  # Bad Request

    if not portfolio:
        return jsonify({"error": "Portfolio ID not found"}), 404  # Not Found

    # Simulate external service failure
    if portfolio == 402:
        return jsonify({"error": "The external service is unavailable. Please try again later."}), 402  # Request Failed
    
    # Check for server errors
    error_response = simulate_server_errors(portfolio, None)
    if error_response:
        return error_response

    return jsonify({
        "status": "OK",
        "portfolio": portfolio
    }), 200  # OK

# New PATCH endpoint: Update portfolio balance
@app.route('/financial-portfolio/<portfolio_id>', methods=['PATCH'])
def update_portfolio(portfolio_id):

    # Validate headers directly
    api_host = request.headers.get('x-api-host')
    api_key = request.headers.get('x-api-key')

    if not api_host or not api_key:
        return jsonify({"error": "Missing required headers 'api_host' or 'api_key"}), 401  # Unauthorized

    if api_host != "finance-data.api.com":
        return jsonify({"error": "Invalid x-api-host"}), 403  # Forbidden

    if api_key != DEFAULT_API_KEY:
        return jsonify({"error": "Invalid API key"}), 403  # Forbidden

    # Check rate limit
    rate_limit_response = check_rate_limit()
    if rate_limit_response:
        return rate_limit_response

    data = request.get_json()

    # Validate required fields in request body
    if not data or not data.get('new_balance'):
        return jsonify({"error": "Missing required field 'new_balance'"}), 400  # Bad Request

    new_balance = data['new_balance']

    # Check if the portfolio exists
    portfolio = portfolios.get(portfolio_id)
    if not portfolio:
        return jsonify({"error": "Portfolio ID not found"}), 404  # Not Found

    # Simulate external service failure
    if portfolio == 402:
        return jsonify({"error": "The external service is unavailable. Please try again later."}), 402  # Request Failed

    # Simulate updating the portfolio balance
    portfolio['initial_balance'] = new_balance
    update_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Check for server errors
    error_response = simulate_server_errors(portfolio_id, new_balance)
    if error_response:
        return error_response

    return jsonify({
        "status": "OK",
        "message": f"Portfolio {portfolio_id} updated successfully",
        "portfolio": {
            "portfolio_id": portfolio_id,
            "new_balance": new_balance,
            "update_time": update_time
        }
    }), 200  # OK

# New DELETE endpoint: Delete a portfolio
@app.route('/financial-portfolio/<portfolio_id>', methods=['DELETE'])
def delete_portfolio(portfolio_id):

    # Validate headers directly
    api_host = request.headers.get('x-api-host')
    api_key = request.headers.get('x-api-key')

    if not api_host or not api_key:
        return jsonify({"error": "Missing required headers 'api_host' or 'api_key'"}), 401  # Unauthorized

    if api_host != "finance-data.api.com":
        return jsonify({"error": "Invalid x-api-host"}), 403  # Forbidden

    if api_key != DEFAULT_API_KEY:
        return jsonify({"error": "Invalid API key"}), 403  # Forbidden

    # Check rate limit
    rate_limit_response = check_rate_limit()
    if rate_limit_response:
        return rate_limit_response

    # Check if the portfolio exists
    if portfolio_id not in portfolios:
        return jsonify({"error": "Portfolio ID not found"}), 404  # Not Found

    # Simulate external service failure
    if portfolio == 402:
        return jsonify({"error": "The external service is unavailable. Please try again later."}), 402  # Request Failed
    
    # Check for server errors
    error_response = simulate_server_errors(portfolio_id, None)
    if error_response:
        return error_response

    # Simulate deleting the portfolio by ID
    deletion_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    del portfolios[portfolio_id]

    return jsonify({
        "status": "OK",
        "message": f"Portfolio {portfolio_id} deleted successfully",
        "deletion_time": deletion_time
    }), 200  # OK

if __name__ == '__main__':
    app.run(port=5000)
