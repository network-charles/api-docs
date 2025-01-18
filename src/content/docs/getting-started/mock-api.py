import os
from flask import Flask, jsonify, request
import time
import datetime
from collections import defaultdict
import random

app = Flask(__name__)

DEFAULT_API_KEY = os.getenv('API_KEY')

@app.route('/get-api-key', methods=['GET'])
def get_api_key():
    return jsonify({
        "success": True,
        "api_key": DEFAULT_API_KEY
    })

# Rate-limiting data structure
request_log = defaultdict(list)
RATE_LIMIT = 5  # Max requests per time window
TIME_WINDOW = 60  # Time window in seconds (e.g., 60 seconds = 1 minute)

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

    # Check for missing query parameters
    if not from_symbol or not to_symbol:
        return jsonify({"error": "Missing required query parameters"}), 400  # Bad Request

    # Simulate external service failure (e.g., unavailable exchange rate service)
    if from_symbol == "SERVICE_UNAVAILABLE" or to_symbol == "SERVICE_UNAVAILABLE":
        return jsonify({"error": "The external service is unavailable. Please try again later."}), 402  # Request Failed

    # Check for conflict: from_symbol is the same as to_symbol
    if from_symbol == to_symbol:
        return jsonify({"error": "Conflict: Cannot exchange the same currency"}), 409  # Conflict

    # Simulate different server errors based on the query parameters
    if from_symbol == "SERVER_500":
        return jsonify({"error": "Internal server error"}), 500  # 500 Internal Server Error
    
    if from_symbol == "SERVER_502":
        return jsonify({"error": "Bad Gateway"}), 502  # 502 Bad Gateway
    
    if from_symbol == "SERVER_503":
        return jsonify({"error": "Service Unavailable"}), 503  # 503 Service Unavailable
    
    if from_symbol == "SERVER_504":
        return jsonify({"error": "Gateway Timeout"}), 504  # 504 Gateway Timeout

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

    data = request.get_json()

    # Validate required fields in request body
    if not data or not data.get('portfolio_name') or not data.get('initial_balance'):
        return jsonify({"error": "Missing required fields"}), 400  # Bad Request
    
    portfolio_name = data['portfolio_name']
    initial_balance = data['initial_balance']

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
        return jsonify({"error": "Missing required headers"}), 401  # Unauthorized

    if api_host != "finance-data.api.com":
        return jsonify({"error": "Invalid x-api-host"}), 403  # Forbidden

    if api_key != DEFAULT_API_KEY:
        return jsonify({"error": "Invalid API key"}), 403  # Forbidden

    # Retrieve the portfolio from the portfolios dictionary
    portfolio = portfolios.get(portfolio_id)

    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404  # Not Found

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
        return jsonify({"error": "Missing required headers"}), 401  # Unauthorized

    if api_host != "finance-data.api.com":
        return jsonify({"error": "Invalid x-api-host"}), 403  # Forbidden

    if api_key != DEFAULT_API_KEY:
        return jsonify({"error": "Invalid API key"}), 403  # Forbidden

    data = request.get_json()

    # Validate required fields in request body
    if not data or not data.get('new_balance'):
        return jsonify({"error": "Missing required field 'new_balance'"}), 400  # Bad Request

    new_balance = data['new_balance']

    # Check if the portfolio exists
    portfolio = portfolios.get(portfolio_id)
    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404  # Not Found

    # Simulate updating the portfolio balance
    portfolio['initial_balance'] = new_balance
    update_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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
        return jsonify({"error": "Missing required headers"}), 401  # Unauthorized

    if api_host != "finance-data.api.com":
        return jsonify({"error": "Invalid x-api-host"}), 403  # Forbidden

    if api_key != DEFAULT_API_KEY:
        return jsonify({"error": "Invalid API key"}), 403  # Forbidden

    # Check if the portfolio exists
    if portfolio_id not in portfolios:
        return jsonify({"error": "Portfolio not found"}), 404  # Not Found

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
