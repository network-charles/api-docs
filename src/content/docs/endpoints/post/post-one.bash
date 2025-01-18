curl -X POST http://127.0.0.1:5000/financial-portfolio \
-H "x-api-host: finance-data.api.com" \
-H "x-api-key: YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "portfolio_name": "Retirement Fund",
    "initial_balance": 50000
}'
