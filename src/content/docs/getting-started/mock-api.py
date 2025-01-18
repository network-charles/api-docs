from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/currency-exchange-rate', methods=['GET'])
def mock_currency_exchange_rate():
    # Get query parameters
    from_symbol = request.args.get('from_symbol')
    to_symbol = request.args.get('to_symbol')
    rapidapi_host = request.headers.get('x-rapidapi-host')
    rapidapi_key = request.headers.get('x-rapidapi-key')

    # Check for missing or invalid headers
    if not rapidapi_host or not rapidapi_key:
        return jsonify({"error": "Missing required headers"}), 401  # Unauthorized

    if rapidapi_host != "finance-data.api.com":
        return jsonify({"error": "Invalid x-rapidapi-host"}), 403  # Forbidden

    if rapidapi_key != "1234567890":
        return jsonify({"error": "Invalid API key"}), 403  # Forbidden

    # Check for missing query parameters
    if not from_symbol or not to_symbol:
        return jsonify({"error": "Missing required query parameters"}), 400  # Bad Request

    # Simulate different responses based on parameters
    if from_symbol == "INVALID" or to_symbol == "INVALID":
        return jsonify({"error": "Invalid parameters"}), 402  # Request Failed

    if from_symbol == "RATE_LIMIT":
        return jsonify({"error": "Too many requests"}), 429  # Too Many Requests

    if from_symbol == "SERVER_ERROR":
        return jsonify({"error": "Internal server error"}), 500  # Server Error

    # Default success response
    return jsonify({
        "status": "OK",
        "request_id": "59f8125c-90a1-4d33-a139-67b83b09017e",
        "data": {
            "from_symbol": from_symbol,
            "to_symbol": to_symbol,
            "type": "currency",
            "exchange_rate": 1560.1323,
            "previous_close": 1553.35,
            "last_update_utc": "2025-01-18 07:35:05"
        }
    }), 200

if __name__ == '__main__':
    app.run(port=5000)
